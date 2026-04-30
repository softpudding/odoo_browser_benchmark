#!/usr/bin/env python3
"""Benchmark evaluation runner — agent-agnostic, parallel-safe.

Supports four evaluation modes:
  - browser-use: automated browser agent
  - oracle: Playwright gold-standard script (proves task is solvable)
  - human: manual testing (prints instruction, waits for Enter)
  - command: any external agent via shell command

The runner handles DB seeding, state capture, and scoring.
The agent just needs to complete the task in the browser.

**Parallel execution:** By default each ``eval.py run`` auto-isolates — it
allocates a free port, creates an ephemeral database, and manages its own
Odoo process.  Multiple runs can execute concurrently with zero coordination.
Pass ``--no-isolate`` to revert to the legacy shared-DB/port behaviour.

Usage (with uv — recommended)::

    # Automated with browser-use (auto-isolated)
    uv run benchmark-eval run <task_dir> --agent browser-use --provider dashscope

    # Run multiple tasks in parallel (each gets its own DB + port)
    uv run benchmark-eval run task_a --agent browser-use &
    uv run benchmark-eval run task_b --agent browser-use &
    wait

    # Human tester
    uv run benchmark-eval run <task_dir> --agent human

    # External agent
    uv run benchmark-eval run <task_dir> --agent command --cmd "python my_agent.py"

    # Legacy single-server mode (shared DB, no isolation)
    uv run benchmark-eval run <task_dir> --no-isolate

    # List all tasks
    uv run benchmark-eval list

    # Re-score a completed run
    uv run benchmark-eval score <output_dir> --task <task_dir>

    # Clean up orphan processes / stale DBs after a crash
    uv run benchmark-eval cleanup

    # First-time setup on a new machine: build the base DB + snapshot
    uv run benchmark-eval bootstrap-base
"""

from __future__ import annotations

import argparse
import atexit
import configparser
import html
import json
import os
import re
import signal
import socket
import subprocess
import sys
import time
from pathlib import Path
from typing import Any
from xmlrpc import client as xmlrpclib

REPO_ROOT = Path(__file__).resolve().parent.parent
BENCHMARK_DIR = REPO_ROOT / "benchmark"
ODOO_BIN = str(REPO_ROOT / "odoo-bin")
ODOO_PYTHON = str(REPO_ROOT / ".venv" / "bin" / "python3")
if not Path(ODOO_PYTHON).exists():
    ODOO_PYTHON = sys.executable
ODOO_CONF = str(REPO_ROOT / ".odoorc.local")

DEFAULT_BASE_URL = os.getenv("ODOO_BASE_URL", "http://127.0.0.1:8069")
DEFAULT_DB = os.getenv("ODOO_DB", "benchmark_validate")
DEFAULT_LOGIN = "admin"
DEFAULT_PASSWORD = "admin"


# ---------------------------------------------------------------------------
# Per-process isolation helpers
# ---------------------------------------------------------------------------

def _find_free_port() -> int:
    """Ask the OS for a free TCP port."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def _write_run_config(run_id: str, port: int, db: str) -> Path:
    """Create a temporary Odoo config with the given port and DB."""
    config = configparser.ConfigParser()
    config.read(ODOO_CONF)
    if not config.has_section("options"):
        config.add_section("options")
    config.set("options", "http_port", str(port))
    config.set("options", "db_name", db)
    path = Path(f"/tmp/bench_odoo_{run_id}.conf")
    with open(path, "w") as f:
        config.write(f)
    return path


class OdooProcess:
    """Manages a single Odoo server process for one eval run."""

    def __init__(self, db: str, port: int, conf: str, run_id: str):
        self.db = db
        self.port = port
        self.conf = conf
        self.run_id = run_id
        self._proc: subprocess.Popen | None = None
        self._log_path = Path(f"/tmp/bench_odoo_{run_id}.log")
        self._pid_path = Path(f"/tmp/bench_odoo_{run_id}.pid")

    def start(self) -> None:
        log_fh = open(self._log_path, "w")
        self._proc = subprocess.Popen(
            [ODOO_PYTHON, ODOO_BIN,
             "-c", self.conf,
             "-d", self.db,
             "--http-port", str(self.port),
             "--no-database-list"],
            stdout=log_fh,
            stderr=subprocess.STDOUT,
        )
        self._pid_path.write_text(str(self._proc.pid))

    def stop(self) -> None:
        if self._proc and self._proc.poll() is None:
            self._proc.terminate()
            try:
                self._proc.wait(timeout=10)
            except subprocess.TimeoutExpired:
                self._proc.kill()
                self._proc.wait()
        self._pid_path.unlink(missing_ok=True)

    def wait_ready(self, timeout: int = 60) -> None:
        import urllib.request
        deadline = time.time() + timeout
        while time.time() < deadline:
            try:
                urllib.request.urlopen(
                    f"http://127.0.0.1:{self.port}/web/login", timeout=2,
                )
                return
            except Exception:
                if self._proc and self._proc.poll() is not None:
                    raise RuntimeError(
                        f"Odoo exited with code {self._proc.returncode}. "
                        f"See {self._log_path}"
                    )
                time.sleep(2)
        raise RuntimeError(f"Odoo not ready after {timeout}s on port {self.port}")


def _cleanup_run(run_id: str, db: str) -> None:
    """Remove all per-run resources (DB, temp files)."""
    from benchmark.db import DatabaseManager
    try:
        DatabaseManager().drop_database(db)
    except Exception:
        pass
    for suffix in (".conf", ".pid", ".log"):
        Path(f"/tmp/bench_odoo_{run_id}{suffix}").unlink(missing_ok=True)


# Global refs for atexit/signal cleanup
_active_odoo_proc: OdooProcess | None = None
_active_run_id: str | None = None
_active_db: str | None = None
_active_keep_db: bool = False


def _emergency_cleanup() -> None:
    if _active_odoo_proc:
        _active_odoo_proc.stop()
    if _active_run_id and _active_db and not _active_keep_db:
        _cleanup_run(_active_run_id, _active_db)


atexit.register(_emergency_cleanup)


# ---------------------------------------------------------------------------
# XML-RPC state reader
# ---------------------------------------------------------------------------

class OdooRPC:
    """Reads Odoo state via XML-RPC. No ORM dependency needed."""

    def __init__(self, base_url: str, db: str, login: str, password: str):
        self.db = db
        self.login = login
        self.password = password
        self.common = xmlrpclib.ServerProxy(f"{base_url}/xmlrpc/2/common")
        self.object = xmlrpclib.ServerProxy(
            f"{base_url}/xmlrpc/2/object", use_datetime=True,
        )
        self.uid = self.common.authenticate(db, login, password, {})
        if not self.uid:
            raise RuntimeError(f"XML-RPC auth failed for {login}@{db}")

    def search_read(
        self, model: str, domain: list, fields: list, **kw
    ) -> list[dict]:
        return self.object.execute_kw(
            self.db, self.uid, self.password,
            model, "search_read", [domain],
            {"fields": fields, **kw},
        )

    def search_count(self, model: str, domain: list) -> int:
        return self.object.execute_kw(
            self.db, self.uid, self.password,
            model, "search_count", [domain],
        )

    def call(self, model: str, method: str, args: list = None, kwargs: dict = None):
        """Call any model method via XML-RPC."""
        return self.object.execute_kw(
            self.db, self.uid, self.password,
            model, method, args or [], kwargs or {},
        )

    def start_trace(self, session_name: str = "") -> dict:
        """Start benchmark trace recording."""
        return self.call("benchmark.trace", "start_trace", [session_name])

    def stop_trace(self) -> dict:
        """Stop benchmark trace recording."""
        return self.call("benchmark.trace", "stop_trace")

    def get_trace(self) -> list[dict]:
        """Retrieve the full trace."""
        return self.call("benchmark.trace", "get_trace")

    def get_trace_summary(self) -> dict:
        """Retrieve trace summary."""
        return self.call("benchmark.trace", "get_trace_summary")

    def read_state(self, state_spec: dict) -> dict[str, list[dict]]:
        """Read all models/fields declared in a state_spec.

        Returns {model_name: [record_dicts]} for each model in the spec.
        """
        result = {}
        for model_name, spec in state_spec.get("models", {}).items():
            fields = spec.get("fields", [])
            ignore = set(spec.get("ignore_fields", []))
            read_fields = [f for f in fields if f not in ignore]
            if not read_fields:
                continue
            records = self.search_read(
                model_name, [], read_fields, context={"active_test": False},
            )
            result[model_name] = records
        return result


# ---------------------------------------------------------------------------
# State diff engine (works on plain dicts, no ORM)
# ---------------------------------------------------------------------------

_HTML_TAG_RE = re.compile(r"</?[A-Za-z][^>]*>")


def _normalize_text(value: str) -> str:
    """Normalize rich-text HTML fragments into stable plain text."""
    if not _HTML_TAG_RE.search(value):
        return value

    text = re.sub(r"(?i)<\s*br\s*/?\s*>", "\n", value)
    text = re.sub(r"(?i)</\s*(p|div|li|tr|h[1-6])\s*>", "\n", text)
    text = re.sub(r"<[^>]+>", "", text)
    text = html.unescape(text).replace("\xa0", " ")
    lines = [" ".join(line.split()) for line in text.splitlines()]
    text = "\n".join(line for line in lines if line)
    return text.strip()


def normalize_value(val: Any) -> Any:
    """Normalize an XML-RPC value for comparison."""
    if val is False:
        return None
    if isinstance(val, (list, tuple)):
        # Many2one: [id, name] -> name
        if len(val) == 2 and isinstance(val[0], int) and isinstance(val[1], str):
            return _normalize_text(val[1])
        # x2many: list of ids -> sorted tuple
        return tuple(sorted(val))
    if isinstance(val, str):
        return _normalize_text(val)
    return val


def build_entity_key(record: dict, match_key: list[str]) -> tuple:
    """Build entity key from a record dict."""
    parts = []
    for f in match_key:
        val = record.get(f)
        parts.append(normalize_value(val))
    return tuple(parts)


def compute_state_diff(
    before: dict[str, list[dict]],
    after: dict[str, list[dict]],
    state_spec: dict,
) -> list[dict]:
    """Compute atomic edits between before and after states.

    Returns list of {model, entity_key, field, op, norm_value} dicts.
    """
    edits = []

    for model_name, spec in state_spec.get("models", {}).items():
        if spec.get("optional"):
            continue

        match_key = spec.get("match_key", ["id"])
        fields = spec.get("fields", [])
        ignore = set(spec.get("ignore_fields", []))
        check_fields = [f for f in fields if f not in ignore]

        before_records = before.get(model_name, [])
        after_records = after.get(model_name, [])

        # Index by entity key
        before_map: dict[tuple, dict] = {}
        key_counts: dict[tuple, int] = {}
        for rec in before_records:
            base_key = build_entity_key(rec, match_key)
            count = key_counts.get(base_key, 0)
            key_counts[base_key] = count + 1
            key = base_key if count == 0 else (*base_key, f"#dup{count}")
            before_map[key] = rec

        after_map: dict[tuple, dict] = {}
        key_counts = {}
        for rec in after_records:
            base_key = build_entity_key(rec, match_key)
            count = key_counts.get(base_key, 0)
            key_counts[base_key] = count + 1
            key = base_key if count == 0 else (*base_key, f"#dup{count}")
            after_map[key] = rec

        # Created records
        for key, rec in after_map.items():
            if key not in before_map:
                for f in check_fields:
                    edits.append({
                        "model": model_name,
                        "entity_key": list(key),
                        "field": f,
                        "op": "create",
                        "norm_value": normalize_value(rec.get(f)),
                    })

        # Deleted records
        for key, rec in before_map.items():
            if key not in after_map:
                for f in check_fields:
                    edits.append({
                        "model": model_name,
                        "entity_key": list(key),
                        "field": f,
                        "op": "delete",
                        "norm_value": normalize_value(rec.get(f)),
                    })

        # Modified records
        for key in after_map:
            if key in before_map:
                for f in check_fields:
                    old = normalize_value(before_map[key].get(f))
                    new = normalize_value(after_map[key].get(f))
                    if old != new:
                        edits.append({
                            "model": model_name,
                            "entity_key": list(key),
                            "field": f,
                            "op": "set",
                            "norm_value": new,
                        })

    return edits


# ---------------------------------------------------------------------------
# Trace evaluation
# ---------------------------------------------------------------------------

def evaluate_trace(trace: list[dict], trace_spec: dict) -> dict:
    """Evaluate the API trace against trace_spec.

    Per the spec, traces are scored by required-op coverage and
    forbidden-op / forbidden-write occurrence, not by a global write
    allowlist. Optional ops are diagnostic only.
    """
    required_ops = set(trace_spec.get("required_ops", []))
    forbidden_ops = set(trace_spec.get("forbidden_ops", []))

    fired_ops = {e["canonical_op"] for e in trace}
    writes = [e for e in trace if e.get("mutation_class") == "write"]

    # Required op recall
    if required_ops:
        required_hits = required_ops & fired_ops
        required_op_recall = len(required_hits) / len(required_ops)
    else:
        required_op_recall = 1.0

    # Explicitly forbidden ops fired
    forbidden_fired = forbidden_ops & fired_ops
    forbidden_write_events = [
        e for e in writes if e["canonical_op"] in forbidden_ops
    ]

    # Write precision: fraction of observed write events that are not forbidden
    if writes:
        non_forbidden_writes = len(writes) - len(forbidden_write_events)
        write_precision = non_forbidden_writes / len(writes)
    else:
        write_precision = 1.0

    # Harmful write rate: forbidden write events / total writes
    harmful_write_rate = len(forbidden_write_events) / max(1, len(writes))

    # StrictSuccess = OutcomeSuccess AND no forbidden op fired.
    strict_clean = len(forbidden_fired) == 0

    return {
        "required_op_recall": round(required_op_recall, 4),
        "write_precision": round(write_precision, 4),
        "harmful_write_rate": round(harmful_write_rate, 4),
        "strict_clean": strict_clean,
        "total_api_calls": len(trace),
        "write_calls": len(writes),
        "read_calls": len(trace) - len(writes),
        "non_forbidden_writes": len(writes) - len(forbidden_write_events),
        "forbidden_write_events": len(forbidden_write_events),
        "required_ops_hit": sorted(required_ops & fired_ops),
        "required_ops_missed": sorted(required_ops - fired_ops),
        "forbidden_ops_fired": sorted(forbidden_fired),
    }


# ---------------------------------------------------------------------------
# Scoring
# ---------------------------------------------------------------------------

def score_run(
    observed_diff: list[dict],
    expected_diff: list[dict],
    wall_clock: float,
    agent_steps: int,
    gave_up: bool = False,
    trace_score: dict | None = None,
    postcondition_failures: list[str] | None = None,
) -> dict:
    """Score a benchmark run.

    Returns the full metric dict including StrictSuccess per spec Section 11.1:
    - OutcomeSuccess: binary exact match on normalized state oracle
    - StrictSuccess: OutcomeSuccess AND no forbidden operation fired
    - StateDiffF1: atomic-edit F1 on the expected state delta
    """
    # Build sets for F1
    def to_tuple(d: dict) -> tuple:
        ek = d.get("entity_key", [])
        if isinstance(ek, list):
            ek = tuple(ek)
        nv = d.get("norm_value")
        if isinstance(nv, list):
            nv = tuple(nv)
        return (d["model"], ek, d["field"], d["op"], nv)

    expected_set = {to_tuple(e) for e in expected_diff}
    observed_set = {to_tuple(e) for e in observed_diff}

    # F1
    if not expected_set and not observed_set:
        precision = recall = f1 = 1.0
    else:
        intersection = expected_set & observed_set
        precision = len(intersection) / len(observed_set) if observed_set else 0.0
        recall = len(intersection) / len(expected_set) if expected_set else 0.0
        f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) > 0 else 0.0

    outcome_success = expected_set == observed_set
    if gave_up:
        outcome_success = False

    # StrictSuccess = OutcomeSuccess AND no forbidden ops fired (spec §11.1)
    strict_clean = trace_score.get("strict_clean", True) if trace_score else True
    strict_success = outcome_success and strict_clean

    if postcondition_failures:
        outcome_success = False
        strict_success = False
        precision = recall = f1 = 0.0

    return {
        "outcome_success": outcome_success,
        "strict_success": strict_success,
        "state_diff_f1": round(f1, 4),
        "state_diff_precision": round(precision, 4),
        "state_diff_recall": round(recall, 4),
        "wall_clock_sec": round(wall_clock, 1),
        "agent_steps": agent_steps,
        "gave_up": gave_up,
        "expected_edits": len(expected_set),
        "observed_edits": len(observed_set),
        "matching_edits": len(expected_set & observed_set),
        "missing_edits": len(expected_set - observed_set),
        "extra_edits": len(observed_set - expected_set),
    }


def run_postconditions(task_dir: Path, db: str, conf_path: str = ODOO_CONF) -> list[str]:
    """Run task-specific postcondition checks from check.py if present."""
    check_file = task_dir / "check.py"
    if not check_file.exists():
        return []

    wrapper = f"""
import json
{check_file.read_text()}
failures = check(self.env)
if not isinstance(failures, list):
    failures = [f"check.py returned non-list: {{type(failures).__name__}}"]
print("CHECK_JSON:" + json.dumps(failures))
"""
    result = subprocess.run(
        [ODOO_PYTHON, ODOO_BIN, "shell", "-c", conf_path, "-d", db, "--no-http"],
        input=wrapper,
        capture_output=True,
        text=True,
        cwd=str(REPO_ROOT),
        timeout=120,
    )

    for line in result.stdout.splitlines():
        if line.startswith("CHECK_JSON:"):
            return json.loads(line[len("CHECK_JSON:"):])

    stderr = result.stderr.strip().splitlines()
    tail = stderr[-3:] if stderr else ["no stderr output"]
    return [f"Postcondition check failed to return JSON: {' | '.join(tail)}"]


# ---------------------------------------------------------------------------
# Task loading
# ---------------------------------------------------------------------------

def load_task(task_dir: Path) -> dict:
    """Load task definition from a directory."""
    import yaml

    task_file = task_dir / "task.yaml"
    task = yaml.safe_load(task_file.read_text()) if task_file.exists() else {}

    # Prompt
    prompt_file = task_dir / "prompt.md"
    if prompt_file.exists():
        task["instruction"] = prompt_file.read_text().strip()

    # State spec
    state_file = task_dir / "state_spec.yaml"
    if state_file.exists():
        task["state_spec"] = yaml.safe_load(state_file.read_text())

    # Expected state
    expected_file = task_dir / "expected_state.json"
    if expected_file.exists():
        task["expected_diff"] = json.loads(expected_file.read_text())

    # Trace spec
    trace_file = task_dir / "trace_spec.yaml"
    if trace_file.exists():
        task["trace_spec"] = yaml.safe_load(trace_file.read_text())

    return task


# ---------------------------------------------------------------------------
# Agent runners
# ---------------------------------------------------------------------------

def run_browser_use(
    instruction: str,
    start_url: str,
    *,
    base_url: str,
    db: str,
    login: str | None,
    password: str | None,
    provider: str = "browser-use",
    model: str | None = None,
    max_steps: int = 200,
    time_limit_sec: int = 300,
    headed: bool = True,
) -> dict:
    """Run browser-use agent and return result."""
    bu_args = [
        ODOO_PYTHON, str(REPO_ROOT / "setup" / "browser_use_local.py"),
        instruction,
        "--base-url", base_url,
        "--start-path", start_url,
        "--db", db,
        "--max-steps", str(max_steps),
        "--provider", provider,
    ]
    if login:
        bu_args.extend(["--login", login])
    if password:
        bu_args.extend(["--password", password])
    if model:
        bu_args.extend(["--model", model])
    if headed:
        bu_args.append("--headed")

    t0 = time.time()
    try:
        result = subprocess.run(
            bu_args,
            capture_output=True,
            text=True,
            cwd=str(REPO_ROOT),
            timeout=time_limit_sec,
        )
        wall_clock = time.time() - t0

        # Parse result from stdout
        stdout = result.stdout
        success = "Task completed successfully" in stdout
        gave_up = "success: False" in stdout or result.returncode != 0

        # Count steps
        steps = stdout.count("📍 Step")

        return {
            "success": success and not gave_up,
            "gave_up": gave_up,
            "wall_clock": wall_clock,
            "steps": steps,
            "stdout": stdout,
            "stderr": result.stderr,
            "returncode": result.returncode,
        }
    except subprocess.TimeoutExpired as exc:
        wall_clock = time.time() - t0
        stdout = exc.stdout.decode() if isinstance(exc.stdout, bytes) else (exc.stdout or "")
        stderr = exc.stderr.decode() if isinstance(exc.stderr, bytes) else (exc.stderr or "")
        return {
            "success": False,
            "gave_up": True,
            "wall_clock": wall_clock,
            "steps": stdout.count("📍 Step"),
            "stdout": stdout,
            "stderr": stderr,
            "returncode": -1,
            "reason": f"timed out after {time_limit_sec}s",
        }


def run_human(
    instruction: str,
    start_url: str,
    *,
    base_url: str,
    login: str | None = None,
    password: str | None = None,
    **kwargs: Any,
) -> dict:
    """Human evaluation mode. Prints instruction, waits for Enter."""
    full_url = f"{base_url.rstrip('/')}{start_url}"

    print()
    print("=" * 70)
    print("  HUMAN EVALUATION MODE")
    print("=" * 70)
    print()
    print("  TIP: Use Chrome Incognito Mode to avoid stale asset cache.")
    print()
    print(f"  URL:      {full_url}")
    if login:
        print(f"  Login:    {login}")
    if password:
        print(f"  Password: {password}")
    print()
    print("  TASK:")
    print("  " + "-" * 66)
    for line in instruction.split("\n"):
        print(f"  {line}")
    print("  " + "-" * 66)
    print()

    t0 = time.time()
    input("  Press ENTER when you have completed the task (or Ctrl+C to abort)...")
    wall_clock = time.time() - t0

    print()
    gave_up = False
    try:
        answer = input("  Did you complete the task successfully? [Y/n]: ").strip().lower()
        if answer in ("n", "no"):
            gave_up = True
    except (EOFError, KeyboardInterrupt):
        gave_up = True

    return {
        "success": not gave_up,
        "gave_up": gave_up,
        "wall_clock": wall_clock,
        "steps": 0,  # not tracked for humans
        "stdout": "",
        "stderr": "",
        "returncode": 0,
    }


def run_command(
    instruction: str,
    start_url: str,
    *,
    base_url: str,
    cmd: str,
    db: str,
    login: str | None,
    password: str | None,
    max_steps: int = 200,
    time_limit_sec: int = 300,
    **kwargs: Any,
) -> dict:
    """Run an external agent command."""
    env = dict(os.environ)
    env.update({
        "BENCHMARK_INSTRUCTION": instruction,
        "BENCHMARK_START_URL": f"{base_url.rstrip('/')}{start_url}",
        "BENCHMARK_BASE_URL": base_url,
        "BENCHMARK_DB": db,
        "BENCHMARK_LOGIN": login or "",
        "BENCHMARK_PASSWORD": password or "",
        "BENCHMARK_MAX_STEPS": str(max_steps),
    })

    t0 = time.time()
    try:
        result = subprocess.run(
            cmd, shell=True, env=env,
            capture_output=True, text=True,
            cwd=str(REPO_ROOT), timeout=time_limit_sec,
        )
        wall_clock = time.time() - t0

        return {
            "success": result.returncode == 0,
            "gave_up": result.returncode != 0,
            "wall_clock": wall_clock,
            "steps": 0,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode,
        }
    except subprocess.TimeoutExpired as exc:
        wall_clock = time.time() - t0
        stdout = exc.stdout.decode() if isinstance(exc.stdout, bytes) else (exc.stdout or "")
        stderr = exc.stderr.decode() if isinstance(exc.stderr, bytes) else (exc.stderr or "")
        return {
            "success": False,
            "gave_up": True,
            "wall_clock": wall_clock,
            "steps": 0,
            "stdout": stdout,
            "stderr": stderr,
            "returncode": -1,
            "reason": f"timed out after {time_limit_sec}s",
        }


def run_oracle(
    instruction: str,
    start_url: str,
    *,
    base_url: str,
    task_dir: Path,
    db: str,
    login: str | None,
    password: str | None,
    time_limit_sec: int = 300,
    headed: bool = True,
    **kwargs: Any,
) -> dict:
    """Run a Playwright oracle script from task_dir/oracle.py."""
    oracle_file = task_dir / "oracle.py"
    if not oracle_file.exists():
        return {
            "success": False,
            "gave_up": True,
            "wall_clock": 0,
            "steps": 0,
            "stdout": "",
            "stderr": f"Oracle script not found: {oracle_file}",
            "returncode": 1,
        }

    env = dict(os.environ)
    env.update({
        "BENCHMARK_BASE_URL": base_url,
        "BENCHMARK_START_URL": start_url,
        "BENCHMARK_DB": db or "",
        "BENCHMARK_LOGIN": login or "",
        "BENCHMARK_PASSWORD": password or "",
        "BENCHMARK_HEADED": "1" if headed else "",
    })

    t0 = time.time()
    try:
        result = subprocess.run(
            [ODOO_PYTHON, str(oracle_file)],
            capture_output=True, text=True,
            cwd=str(REPO_ROOT), timeout=time_limit_sec,
            env=env,
        )
        wall_clock = time.time() - t0

        return {
            "success": result.returncode == 0,
            "gave_up": result.returncode != 0,
            "wall_clock": wall_clock,
            "steps": 0,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode,
        }
    except subprocess.TimeoutExpired as exc:
        wall_clock = time.time() - t0
        stdout = exc.stdout.decode() if isinstance(exc.stdout, bytes) else (exc.stdout or "")
        stderr = exc.stderr.decode() if isinstance(exc.stderr, bytes) else (exc.stderr or "")
        return {
            "success": False,
            "gave_up": True,
            "wall_clock": wall_clock,
            "steps": 0,
            "stdout": stdout,
            "stderr": stderr,
            "returncode": -1,
            "reason": f"timed out after {time_limit_sec}s",
        }


# ---------------------------------------------------------------------------
# Seed runner
# ---------------------------------------------------------------------------

def run_seed(task_dir: Path, db: str, rpc: OdooRPC | None = None, conf_path: str = ODOO_CONF) -> None:
    """Run the task's seed.py via odoo shell.

    Also runs cleanup.py first if it exists, to reset state from
    previous runs.
    """
    shell_conf = conf_path if Path(conf_path).exists() else ODOO_CONF

    # Run cleanup first if available
    cleanup_file = task_dir / "cleanup.py"
    if cleanup_file.exists():
        cleanup_code = cleanup_file.read_text()
        cleanup_wrapper = f"""
{cleanup_code}
cleanup(self.env)
self.env.cr.commit()
print('CLEANUP_OK')
"""
        result = subprocess.run(
            [ODOO_PYTHON, ODOO_BIN, "shell", "-c", shell_conf, "-d", db, "--no-http"],
            input=cleanup_wrapper, capture_output=True, text=True,
            cwd=str(REPO_ROOT), timeout=120,
        )
        if "CLEANUP_OK" in result.stdout:
            print("   Cleanup: done")

    seed_file = task_dir / "seed.py"
    if not seed_file.exists():
        return

    seed_code = seed_file.read_text()
    wrapper = f"""
{seed_code}
setup(self.env)
self.env.cr.commit()
print('SEED_OK')
"""
    result = subprocess.run(
        [ODOO_PYTHON, ODOO_BIN, "shell", "-c", shell_conf, "-d", db, "--no-http"],
        input=wrapper, capture_output=True, text=True,
        cwd=str(REPO_ROOT), timeout=120,
    )
    if "SEED_OK" not in result.stdout:
        print(f"  WARNING: seed may have failed")
        if result.stderr:
            print(f"  stderr (last 3 lines): {result.stderr.strip().splitlines()[-3:]}")


# ---------------------------------------------------------------------------
# Episode preparation: clean DB restore + seed + Odoo restart
# ---------------------------------------------------------------------------

SNAPSHOT_DIR = Path(os.getenv("BENCHMARK_SNAPSHOT_DIR", "/tmp/benchmark_snapshots"))
BASE_SNAPSHOT = "benchmark_base"
BASE_MODULES_FILE = BENCHMARK_DIR / "base_modules.txt"


def _load_base_modules() -> list[str]:
    """Read the pinned root-module list for the base snapshot.

    Comments (``# ...``) and blank lines are ignored.
    """
    if not BASE_MODULES_FILE.exists():
        raise FileNotFoundError(
            f"Base module list not found: {BASE_MODULES_FILE}. "
            f"This file pins the modules installed in the benchmark base DB."
        )
    modules = []
    for line in BASE_MODULES_FILE.read_text().splitlines():
        line = line.split("#", 1)[0].strip()
        if line:
            modules.append(line)
    if not modules:
        raise RuntimeError(f"No modules listed in {BASE_MODULES_FILE}")
    return modules


def _prepare_episode(
    db: str,
    task_dir: Path,
    base_url: str,
    *,
    snapshot_name: str | None = None,
    odoo_proc: OdooProcess | None = None,
    conf_path: str = ODOO_CONF,
) -> None:
    """Restore a clean database, seed task data, and restart Odoo.

    This ensures every episode starts from identical state per spec §16:
    'start each episode from a fresh database clone or snapshot restore'.

    When *odoo_proc* is provided (parallel / auto-isolate mode), only
    that process is stopped and restarted.  Otherwise falls back to the
    legacy ``pkill -f odoo-bin`` behaviour.
    """
    from benchmark.db import DatabaseManager
    dbm = DatabaseManager()
    restore_snapshot = snapshot_name or BASE_SNAPSHOT

    # Step 1: Check base snapshot exists
    if restore_snapshot not in dbm.list_snapshots():
        if restore_snapshot == BASE_SNAPSHOT:
            print(f"   No base snapshot '{BASE_SNAPSHOT}' found. Creating from current DB...")
            _create_base_snapshot(db, dbm)
        else:
            raise RuntimeError(
                f"Task snapshot '{restore_snapshot}' not found in {SNAPSHOT_DIR}"
            )

    # Step 2: Stop Odoo — only THIS run's process when isolated
    print("   Stopping Odoo...")
    if odoo_proc:
        odoo_proc.stop()
    else:
        subprocess.run(["pkill", "-f", "odoo-bin"], capture_output=True)
        time.sleep(2)

    # Step 3: Restore clean DB from snapshot
    print(f"   Restoring {db} from snapshot '{restore_snapshot}'...")
    dbm.restore_snapshot(restore_snapshot, db)

    # Step 3b: Clear compiled asset bundles so Odoo regenerates them.
    # pg_restore brings ir_attachment records that reference compiled
    # JS/CSS bundles, but the filestore files don't exist for this DB.
    # Without this, every page load shows AssetsLoadingError.
    print("   Clearing asset cache...")
    subprocess.run(
        ["psql", "-U", dbm.db_user, db, "-c",
         "DELETE FROM ir_attachment WHERE res_model='ir.ui.view' OR url LIKE '/web/assets/%';"],
        capture_output=True, env=dbm._pg_env(),
    )
    # Also copy filestore from source if it exists, or just let Odoo rebuild
    import shutil
    filestore_dir = Path(ODOO_CONF).parent / ".odoo-data" / "filestore"
    target_fs = filestore_dir / db
    if not target_fs.exists():
        target_fs.mkdir(parents=True, exist_ok=True)

    # Step 4: Run seed.py
    print("   Running seed script...")
    run_seed(task_dir, db, conf_path=conf_path)

    # Step 5: Restart Odoo
    print("   Starting Odoo...")
    if odoo_proc:
        if not Path(odoo_proc.conf).exists():
            odoo_proc.conf = ODOO_CONF
        odoo_proc.start()
        odoo_proc.wait_ready()
        print(f"   Odoo ready on port {odoo_proc.port}")
    else:
        subprocess.Popen(
            [ODOO_PYTHON, ODOO_BIN, "-c", ODOO_CONF, "-d", db],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
        # Wait for Odoo to be ready
        import urllib.request
        for i in range(30):
            try:
                urllib.request.urlopen(f"{base_url}/web/login", timeout=2)
                print(f"   Odoo ready ({i*2}s)")
                return
            except Exception:
                time.sleep(2)
        print("   WARNING: Odoo may not be ready (timeout)")


def _create_base_snapshot(db: str, dbm: Any = None) -> None:
    """Create the base snapshot from the current database.

    This should be run once after installing all needed modules
    (sale, project, website_hr_recruitment, benchmark_trace, etc.).
    """
    if dbm is None:
        from benchmark.db import DatabaseManager
        dbm = DatabaseManager()

    SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)
    dbm.create_snapshot(db, BASE_SNAPSHOT)
    print(f"   Base snapshot created: {SNAPSHOT_DIR / (BASE_SNAPSHOT + '.dump')}")


def cmd_prepare_base(args: argparse.Namespace) -> None:
    """Create the base snapshot from the current database state.

    Run this once after installing all needed modules:
      uv run benchmark-eval prepare-base --db benchmark_validate
    """
    from benchmark.db import DatabaseManager
    dbm = DatabaseManager()
    _create_base_snapshot(args.db, dbm)
    print(f"Done. All future eval runs will restore from this snapshot.")


def cmd_bootstrap_base(args: argparse.Namespace) -> None:
    """Build the benchmark base DB and snapshot from scratch.

    Reads the pinned root-module list from ``benchmark/base_modules.txt``,
    installs them into a freshly-created database via ``odoo-bin -i``, then
    dumps the snapshot to ``BENCHMARK_SNAPSHOT_DIR``.  Idempotent in the
    sense that re-running with ``--rebuild`` always produces a snapshot
    matching the current pinned module list.

    Use this on a new machine, or after editing ``base_modules.txt``::

        uv run benchmark-eval bootstrap-base                # safe: refuses if DB exists
        uv run benchmark-eval bootstrap-base --rebuild      # drop + recreate
    """
    from benchmark.db import DatabaseManager

    db = args.db
    modules = _load_base_modules()
    dbm = DatabaseManager()

    print(f"=== Bootstrap benchmark base DB ===")
    print(f"  DB:       {db}")
    print(f"  Modules:  {len(modules)} root ({', '.join(modules)})")
    print(f"  Snapshot: {SNAPSHOT_DIR / (BASE_SNAPSHOT + '.dump')}")
    print()

    # 1. Handle existing DB
    if dbm.database_exists(db):
        if not args.rebuild:
            print(
                f"ERROR: Database '{db}' already exists. "
                f"Pass --rebuild to drop and recreate it, "
                f"or run 'prepare-base --db {db}' to snapshot it as-is."
            )
            sys.exit(1)
        print(f"  Dropping existing '{db}'...")
        dbm.drop_database(db)

    # 2. Create empty DB
    print(f"  Creating '{db}'...")
    result = subprocess.run(
        ["createdb", db], env=dbm._pg_env(), capture_output=True, text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(f"createdb failed: {result.stderr}")

    # 3. Install modules via odoo-bin
    print(f"  Installing modules (this takes a few minutes)...")
    log_path = Path(f"/tmp/bench_bootstrap_{db}.log")
    with open(log_path, "w") as log_fh:
        result = subprocess.run(
            [ODOO_PYTHON, ODOO_BIN,
             "-c", ODOO_CONF, "-d", db,
             "-i", ",".join(modules),
             "--stop-after-init", "--no-http"],
            stdout=log_fh, stderr=subprocess.STDOUT,
            cwd=str(REPO_ROOT),
        )
    if result.returncode != 0:
        print(f"ERROR: odoo-bin -i failed (exit {result.returncode}). See {log_path}")
        sys.exit(1)
    print(f"  Module install log: {log_path}")

    # 4. Verify benchmark_trace landed (it gates trace recording)
    check = subprocess.run(
        ["psql", "-U", dbm.db_user, "-d", db, "-tAc",
         "SELECT count(*) FROM ir_module_module "
         "WHERE name='benchmark_trace' AND state='installed'"],
        env=dbm._pg_env(), capture_output=True, text=True,
    )
    if check.stdout.strip() != "1":
        print(
            f"ERROR: benchmark_trace did not install. "
            f"API trace recording will be unavailable. See {log_path}"
        )
        sys.exit(1)

    # 5. Snapshot
    print(f"  Dumping snapshot...")
    _create_base_snapshot(db, dbm)
    print()
    print(f"Done. All future eval runs will restore from this snapshot.")


# ---------------------------------------------------------------------------
# Main evaluation flow
# ---------------------------------------------------------------------------

def cmd_run(args: argparse.Namespace) -> dict | None:
    """Run a benchmark task end-to-end with proper instrumentation.

    Returns the score dict on success, or *None* on early error.

    When ``--no-isolate`` is **not** set and the user did not provide
    explicit ``--db`` / ``--base-url``, the run auto-isolates: it picks
    a free port, creates an ephemeral database, and manages its own
    Odoo process.  This lets multiple ``eval.py run`` invocations
    execute concurrently without collisions.
    """
    global _active_odoo_proc, _active_run_id, _active_db, _active_keep_db

    task_dir = Path(args.task_dir)
    if not task_dir.is_absolute():
        task_dir = BENCHMARK_DIR / "tasks" / args.task_dir

    if not task_dir.exists():
        print(f"ERROR: Task directory not found: {task_dir}")
        print(f"  Available tasks:")
        for td in sorted((BENCHMARK_DIR / "tasks").iterdir()):
            if (td / "task.yaml").exists():
                print(f"    {td.name}")
        return None

    task = load_task(task_dir)
    state_spec = task.get("state_spec", {})
    expected_diff = task.get("expected_diff", [])
    instruction = task.get("instruction", "")
    start_url = task.get("start_url", "/odoo")
    task_id = task.get("task_id", task_dir.name)
    login_context = task.get("login_context", {}) or {}
    db_seed = task.get("db_seed", {}) or {}
    snapshot_name = db_seed.get("snapshot")

    if args.login is not None:
        agent_login = args.login
    elif "login" in login_context:
        agent_login = login_context.get("login")
    else:
        agent_login = DEFAULT_LOGIN

    if args.password is not None:
        agent_password = args.password
    elif "password" in login_context:
        agent_password = login_context.get("password")
    elif agent_login is None:
        agent_password = None
    else:
        agent_password = DEFAULT_PASSWORD

    rpc_login = DEFAULT_LOGIN
    rpc_password = DEFAULT_PASSWORD
    max_steps = args.max_steps if args.max_steps is not None else task.get("step_limit", 200)
    time_limit_sec = int(
        os.environ.get("BENCHMARK_TIME_LIMIT_SEC", task.get("time_limit_sec", 300))
    )

    if not instruction:
        print(f"ERROR: No instruction found for task {task_id}")
        print(f"  Check that {task_dir}/prompt.md exists")
        return None

    if not expected_diff and not state_spec.get("models"):
        print(f"ERROR: No expected state oracle for task {task_id}")
        print(f"  Need expected_state.json or state_spec.yaml with models")
        return None

    # --- Auto-isolation setup ---
    # When the user did not override --db / --base-url AND did not pass
    # --no-isolate, we spin up an isolated Odoo instance on a free port
    # with its own ephemeral database.
    no_isolate = getattr(args, "no_isolate", False)
    keep_db = getattr(args, "keep_db", False)
    keep_server = getattr(args, "keep_server", False)
    explicit_db = (args.db != DEFAULT_DB)
    explicit_url = (args.base_url != DEFAULT_BASE_URL)
    # Auto-isolation gives this run its own Odoo process on a free port +
    # its own per-run config. It's disabled ONLY if the caller explicitly
    # opts out (--no-isolate) or points at an external Odoo (--base-url).
    # Passing --db on its own does NOT disable isolation — callers often
    # want to control the DB name (e.g. keep it short enough for Postgres)
    # while still getting port/process isolation so concurrent runs don't
    # tromp on each other.
    auto_isolate = not no_isolate and not explicit_url

    odoo_proc: OdooProcess | None = None
    run_id: str | None = None
    conf_path = ODOO_CONF

    if auto_isolate:
        run_id = f"{os.getpid()}_{int(time.time()) % 100000}"
        port = _find_free_port()
        # Respect --db when explicit; otherwise generate a unique-per-run
        # name. Auto-generated names are long enough for some task IDs to
        # exceed Postgres's 63-char DB-name limit, so explicit override is
        # sometimes required.
        db = args.db if explicit_db else f"benchmark_{task_id}_{run_id}"
        base_url = f"http://127.0.0.1:{port}"
        conf_path = str(_write_run_config(run_id, port, db))
        odoo_proc = OdooProcess(db, port, conf_path, run_id)
        # Register for emergency cleanup
        _active_odoo_proc = odoo_proc
        _active_run_id = run_id
        _active_db = db
        _active_keep_db = keep_db
    else:
        db = args.db
        base_url = args.base_url

    # Output dir
    output_dir = Path(args.output_dir) if args.output_dir else (
        BENCHMARK_DIR / "reports" / "runs" / f"{task_id}__{args.agent}__{int(time.time())}"
    )
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"=== Benchmark Evaluation ===")
    print(f"  Task:   {task_id}")
    print(f"  Agent:  {args.agent}")
    if auto_isolate:
        print(f"  DB:     {db}  (auto-isolated)")
        print(f"  URL:    {base_url}")
    else:
        print(f"  DB:     {db}")
        print(f"  URL:    {base_url}")
    print(f"  Output: {output_dir}")
    print()

    try:
        return _run_episode(
            task_dir=task_dir,
            task=task,
            task_id=task_id,
            state_spec=state_spec,
            expected_diff=expected_diff,
            instruction=instruction,
            start_url=start_url,
            snapshot_name=snapshot_name,
            db=db,
            base_url=base_url,
            conf_path=conf_path,
            odoo_proc=odoo_proc,
            agent=args.agent,
            agent_login=agent_login,
            agent_password=agent_password,
            rpc_login=rpc_login,
            rpc_password=rpc_password,
            max_steps=max_steps,
            time_limit_sec=time_limit_sec,
            args=args,
            output_dir=output_dir,
        )
    finally:
        # Cleanup isolated resources
        if odoo_proc and not keep_server:
            odoo_proc.stop()
        if auto_isolate and not keep_db and run_id:
            _cleanup_run(run_id, db)
        # Clear global refs
        _active_odoo_proc = None
        _active_run_id = None
        _active_db = None


def _run_episode(
    *,
    task_dir: Path,
    task: dict,
    task_id: str,
    state_spec: dict,
    expected_diff: list,
    instruction: str,
    start_url: str,
    snapshot_name: str | None,
    db: str,
    base_url: str,
    conf_path: str,
    odoo_proc: OdooProcess | None,
    agent: str,
    agent_login: str | None,
    agent_password: str | None,
    rpc_login: str,
    rpc_password: str,
    max_steps: int,
    time_limit_sec: int,
    args: argparse.Namespace,
    output_dir: Path,
) -> dict:
    """Core evaluation logic, extracted so cmd_run can wrap it with cleanup."""

    # 1. Restore clean DB, seed, and restart Odoo
    print("1. Preparing clean database...")
    _prepare_episode(
        db,
        task_dir,
        base_url,
        snapshot_name=snapshot_name,
        odoo_proc=odoo_proc,
        conf_path=conf_path,
    )
    print("   Done.")

    # 2. Capture before-state and start trace
    print("2. Capturing pre-task state...")
    rpc = OdooRPC(base_url, db, rpc_login, rpc_password)
    before_state = rpc.read_state(state_spec)
    print(f"   Captured {sum(len(v) for v in before_state.values())} records across {len(before_state)} models")

    # Start API trace recording
    trace_available = False
    try:
        rpc.start_trace(task_id)
        trace_available = True
        print("   API trace recording: STARTED")
    except Exception as exc:
        print(f"   API trace recording: UNAVAILABLE ({exc})")
        print(f"   (Install benchmark_trace addon: odoo-bin -d {db} -i benchmark_trace --stop-after-init)")

    # 3. Run agent
    print(f"3. Running agent ({agent})...")
    print()

    if agent == "browser-use":
        agent_result = run_browser_use(
            instruction, start_url,
            base_url=base_url, db=db,
            login=agent_login, password=agent_password,
            provider=args.provider or "browser-use",
            model=args.model,
            max_steps=max_steps,
            time_limit_sec=time_limit_sec,
            headed=args.headed,
        )
    elif agent == "human":
        agent_result = run_human(
            instruction, start_url,
            base_url=base_url,
            login=agent_login,
            password=agent_password,
        )
    elif agent == "oracle":
        agent_result = run_oracle(
            instruction, start_url,
            base_url=base_url, task_dir=task_dir,
            db=db, login=agent_login, password=agent_password,
            time_limit_sec=time_limit_sec,
            headed=args.headed,
        )
    elif agent == "command":
        if not args.cmd:
            print("ERROR: --cmd required for command agent")
            return {}
        agent_result = run_command(
            instruction, start_url,
            base_url=base_url, cmd=args.cmd,
            db=db, login=agent_login, password=agent_password,
            max_steps=max_steps,
            time_limit_sec=time_limit_sec,
        )
    else:
        print(f"ERROR: Unknown agent type: {agent}")
        return {}

    print()
    print(f"   Agent finished: steps={agent_result['steps']}, "
          f"wall_clock={agent_result['wall_clock']:.1f}s, "
          f"success={agent_result['success']}")

    # 4. Stop trace and capture after-state
    print("4. Capturing post-task state and API trace...")
    rpc = OdooRPC(base_url, db, rpc_login, rpc_password)

    # Retrieve API trace
    trace = []
    trace_summary = {}
    if trace_available:
        try:
            rpc.stop_trace()
            trace = rpc.get_trace()
            trace_summary = rpc.get_trace_summary()
            print(f"   API trace: {len(trace)} calls captured "
                  f"({trace_summary.get('write_calls', 0)} writes, "
                  f"{trace_summary.get('read_calls', 0)} reads)")
        except Exception as exc:
            print(f"   API trace retrieval failed: {exc}")

    after_state = rpc.read_state(state_spec)
    print(f"   State: {sum(len(v) for v in after_state.values())} records across {len(after_state)} models")

    # 5. Compute state diff
    print("5. Computing state diff...")
    observed_diff = compute_state_diff(before_state, after_state, state_spec)
    print(f"   {len(observed_diff)} atomic edits observed")

    # 5b. Evaluate trace against trace_spec
    trace_spec = task.get("trace_spec", {})
    trace_score = evaluate_trace(trace, trace_spec) if trace else {}

    # 5c. Run task-specific postcondition checks
    postcondition_failures = run_postconditions(task_dir, db, conf_path=conf_path)
    if postcondition_failures:
        print(f"   Postconditions: {len(postcondition_failures)} failure(s)")

    # 6. Score
    print("6. Scoring...")
    score = score_run(
        observed_diff=observed_diff,
        expected_diff=expected_diff,
        wall_clock=agent_result["wall_clock"],
        agent_steps=agent_result["steps"],
        gave_up=agent_result["gave_up"],
        trace_score=trace_score if trace_score else None,
        postcondition_failures=postcondition_failures,
    )
    # Merge trace metrics into score
    score.update(trace_score)

    # 7. Write artifacts
    (output_dir / "score.json").write_text(json.dumps(score, indent=2))
    (output_dir / "state_diff.json").write_text(json.dumps(observed_diff, indent=2))
    (output_dir / "expected_state.json").write_text(json.dumps(expected_diff, indent=2))
    (output_dir / "trace.json").write_text(json.dumps(trace, indent=2))
    (output_dir / "trace_summary.json").write_text(json.dumps(trace_summary, indent=2, default=str))
    (output_dir / "postcondition_failures.json").write_text(json.dumps(postcondition_failures, indent=2))
    (output_dir / "before_state.json").write_text(json.dumps(
        {k: v for k, v in before_state.items()}, indent=2, default=str,
    ))
    (output_dir / "after_state.json").write_text(json.dumps(
        {k: v for k, v in after_state.items()}, indent=2, default=str,
    ))
    (output_dir / "agent_result.json").write_text(json.dumps({
        k: v for k, v in agent_result.items() if k != "stdout"
    }, indent=2, default=str))
    (output_dir / "agent_stdout.txt").write_text(agent_result.get("stdout", ""))

    # 8. Report
    print()
    print("=" * 50)
    outcome = "PASS" if score["outcome_success"] else "FAIL"
    strict = "PASS" if score["strict_success"] else "FAIL"
    print(f"  RESULT: {outcome}  (Strict: {strict})")
    print(f"  StateDiffF1:  {score['state_diff_f1']}")
    print(f"  Precision:    {score['state_diff_precision']}")
    print(f"  Recall:       {score['state_diff_recall']}")
    print(f"  Expected:     {score['expected_edits']} edits")
    print(f"  Observed:     {score['observed_edits']} edits")
    print(f"  Matching:     {score['matching_edits']} edits")
    print(f"  Missing:      {score['missing_edits']} edits")
    print(f"  Extra:        {score['extra_edits']} edits")
    print(f"  Wall clock:   {score['wall_clock_sec']}s")
    print(f"  Steps:        {score['agent_steps']}")
    print(f"  Gave up:      {score['gave_up']}")
    if trace_score:
        print(f"  --- API Trace ---")
        print(f"  RequiredOpRecall:  {score.get('required_op_recall', 'N/A')}")
        print(f"  WritePrecision:    {score.get('write_precision', 'N/A')}")
        print(f"  HarmfulWriteRate:  {score.get('harmful_write_rate', 'N/A')}")
        print(f"  StrictClean:       {score.get('strict_clean', 'N/A')}")
        print(f"  Total API calls:   {score.get('total_api_calls', 0)}")
        print(f"  Writes:            {score.get('non_forbidden_writes', 0)} non-forbidden, "
              f"{score.get('forbidden_write_events', 0)} forbidden")
        if score.get("required_ops_missed"):
            print(f"  Required ops MISSED: {score['required_ops_missed']}")
        if score.get("forbidden_ops_fired"):
            print(f"  Forbidden ops FIRED: {score['forbidden_ops_fired']}")
    print("=" * 50)
    print(f"  Artifacts: {output_dir}/")
    print()

    if postcondition_failures:
        print("  Postcondition failures:")
        for failure in postcondition_failures:
            print(f"    - {failure}")

    if score["missing_edits"] > 0:
        print("  Missing expected edits:")
        expected_set = {json.dumps(e, sort_keys=True) for e in expected_diff}
        observed_set = {json.dumps(e, sort_keys=True) for e in observed_diff}
        for e in sorted(expected_set - observed_set):
            d = json.loads(e)
            print(f"    - {d['model']}.{d['field']} = {d['norm_value']}")
    if score["extra_edits"] > 0:
        print("  Unexpected extra edits:")
        expected_set = {json.dumps(e, sort_keys=True) for e in expected_diff}
        observed_set = {json.dumps(e, sort_keys=True) for e in observed_diff}
        for e in sorted(observed_set - expected_set):
            d = json.loads(e)
            print(f"    + {d['model']}.{d['field']} = {d['norm_value']}")

    return score


def cmd_list(args: argparse.Namespace) -> None:
    """List all benchmark tasks."""
    import yaml
    tasks_dir = BENCHMARK_DIR / "tasks"
    for td in sorted(tasks_dir.iterdir()):
        tf = td / "task.yaml"
        if tf.exists():
            t = yaml.safe_load(tf.read_text())
            diff = t.get("difficulty", "?")
            has_oracle = (td / "expected_state.json").exists()
            print(f"  {t.get('task_id', td.name):<55s} difficulty={diff:<8s} oracle={'yes' if has_oracle else 'NO'}")


def cmd_cleanup(args: argparse.Namespace) -> None:
    """Kill orphan benchmark Odoo processes and drop stale ephemeral DBs."""
    from benchmark.db import DatabaseManager

    # Kill orphan Odoo processes via stale PID files
    killed = 0
    for pid_file in Path("/tmp").glob("bench_odoo_*.pid"):
        try:
            pid = int(pid_file.read_text().strip())
            os.kill(pid, signal.SIGTERM)
            print(f"  Killed orphan Odoo (PID {pid})")
            killed += 1
        except (ProcessLookupError, ValueError):
            pass
        pid_file.unlink(missing_ok=True)

    # Clean up temp config and log files
    for f in Path("/tmp").glob("bench_odoo_*"):
        f.unlink(missing_ok=True)

    # Drop stale ephemeral benchmark DBs
    dbm = DatabaseManager()
    result = subprocess.run(
        ["psql", "-tAc",
         "SELECT datname FROM pg_database WHERE datname LIKE 'benchmark_%_%'",
         "postgres"],
        capture_output=True, text=True, env=dbm._pg_env(),
    )
    dropped = 0
    for db_name in result.stdout.strip().splitlines():
        db_name = db_name.strip()
        if not db_name or db_name == DEFAULT_DB:
            continue
        # Only drop DBs that look like auto-isolated runs (contain PID_timestamp)
        # Pattern: benchmark_{task_id}_{pid}_{ts}
        parts = db_name.rsplit("_", 2)
        if len(parts) >= 3 and parts[-1].isdigit() and parts[-2].isdigit():
            try:
                dbm.drop_database(db_name)
                print(f"  Dropped stale DB: {db_name}")
                dropped += 1
            except Exception as exc:
                print(f"  Failed to drop {db_name}: {exc}")

    if killed == 0 and dropped == 0:
        print("  No orphan processes or stale databases found.")


def cmd_score(args: argparse.Namespace) -> None:
    """Re-score a completed run."""
    run_dir = Path(args.run_dir)
    task_dir = Path(args.task_dir)
    if not task_dir.is_absolute():
        task_dir = BENCHMARK_DIR / "tasks" / args.task_dir

    task = load_task(task_dir)
    expected_diff = task.get("expected_diff", [])

    observed_diff = json.loads((run_dir / "state_diff.json").read_text())
    agent = json.loads((run_dir / "agent_result.json").read_text())

    score = score_run(
        observed_diff=observed_diff,
        expected_diff=expected_diff,
        wall_clock=agent.get("wall_clock", 0),
        agent_steps=agent.get("steps", 0),
        gave_up=agent.get("gave_up", False),
    )
    print(json.dumps(score, indent=2))


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        prog="benchmark/eval.py",
        description="Odoo Browser Agent Benchmark — Evaluation Runner",
    )
    sub = parser.add_subparsers(dest="command")

    # run
    run_p = sub.add_parser("run", help="Run a benchmark task")
    run_p.add_argument("task_dir", help="Task directory (name or path)")
    run_p.add_argument("--agent", choices=("browser-use", "human", "command", "oracle"),
                       default="browser-use", help="Agent type")
    run_p.add_argument("--cmd", help="Command for 'command' agent type")
    run_p.add_argument("--provider", help="LLM provider for browser-use")
    run_p.add_argument("--model", help="Model override for browser-use")
    run_p.add_argument("--max-steps", type=int, default=None)
    run_p.add_argument("--headed", action="store_true", default=True)
    run_p.add_argument("--headless", action="store_true")
    run_p.add_argument("--base-url", default=DEFAULT_BASE_URL)
    run_p.add_argument("--db", default=DEFAULT_DB)
    run_p.add_argument("--login", default=None)
    run_p.add_argument("--password", default=None)
    run_p.add_argument("--output-dir", help="Custom output directory")
    run_p.add_argument("--no-isolate", action="store_true",
                       help="Disable auto-isolation (use shared DB/port, legacy mode)")
    run_p.add_argument("--keep-db", action="store_true",
                       help="Don't drop the ephemeral database after completion")
    run_p.add_argument("--keep-server", action="store_true",
                       help="Don't stop the Odoo server after completion (for debugging)")

    # list
    sub.add_parser("list", help="List benchmark tasks")

    # prepare-base
    prep_p = sub.add_parser("prepare-base", help="Create base DB snapshot")
    prep_p.add_argument("--db", default=DEFAULT_DB)

    # bootstrap-base
    boot_p = sub.add_parser(
        "bootstrap-base",
        help="Build the benchmark base DB from scratch and snapshot it",
    )
    boot_p.add_argument("--db", default=DEFAULT_DB,
                        help=f"DB name to create (default: {DEFAULT_DB})")
    boot_p.add_argument("--rebuild", action="store_true",
                        help="Drop the DB if it already exists")

    # cleanup
    sub.add_parser("cleanup", help="Kill orphan benchmark processes and drop stale DBs")

    # score
    score_p = sub.add_parser("score", help="Re-score a completed run")
    score_p.add_argument("run_dir")
    score_p.add_argument("--task-dir", required=True)

    args = parser.parse_args()

    if args.command == "run":
        if args.headless:
            args.headed = False
        cmd_run(args)
    elif args.command == "list":
        cmd_list(args)
    elif args.command == "prepare-base":
        cmd_prepare_base(args)
    elif args.command == "bootstrap-base":
        cmd_bootstrap_base(args)
    elif args.command == "cleanup":
        cmd_cleanup(args)
    elif args.command == "score":
        cmd_score(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
