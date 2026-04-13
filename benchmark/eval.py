#!/usr/bin/env python3
"""Benchmark evaluation runner — agent-agnostic.

Supports three evaluation modes:
  - browser-use: automated browser agent
  - human: manual testing (prints instruction, waits for Enter)
  - command: any external agent via shell command

The runner handles DB seeding, state capture, and scoring.
The agent just needs to complete the task in the browser.

Usage::

    # Automated with browser-use
    python benchmark/eval.py run <task_dir> --agent browser-use --provider dashscope

    # Human tester
    python benchmark/eval.py run <task_dir> --agent human

    # External agent
    python benchmark/eval.py run <task_dir> --agent command --cmd "python my_agent.py"

    # List all tasks
    python benchmark/eval.py list

    # Re-score a completed run
    python benchmark/eval.py score <output_dir> --task <task_dir>
"""

from __future__ import annotations

import argparse
import json
import os
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
            records = self.search_read(model_name, [], read_fields)
            result[model_name] = records
        return result


# ---------------------------------------------------------------------------
# State diff engine (works on plain dicts, no ORM)
# ---------------------------------------------------------------------------

def normalize_value(val: Any) -> Any:
    """Normalize an XML-RPC value for comparison."""
    if val is False:
        return None
    if isinstance(val, (list, tuple)):
        # Many2one: [id, name] -> name
        if len(val) == 2 and isinstance(val[0], int) and isinstance(val[1], str):
            return val[1]
        # x2many: list of ids -> sorted tuple
        return tuple(sorted(val))
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

# Framework write ops that always occur during normal Odoo usage.
# These are NOT agent actions — they're bootstrap/session/notification
# operations that fire on every page load. Excluded from write allowlist
# enforcement to avoid false positives.
FRAMEWORK_WRITE_OPS = frozenset({
    # Session / login
    "custom:/web/login",
    "custom:/web/session/authenticate",
    # Navigation / menu loading (POST in Odoo)
    "custom:/web/action/load",
    "custom:/web/webclient/load_menus",
    "custom:/web/webclient/translations",
    "custom:/website/translations",
    # Mail / push notifications
    "custom:/mail/data",
    "custom:/mail/thread/messages",
    "custom:/mail/action",
    "custom:/mail/link_preview",
    "mail.push.device.register_devices",
    "mail.push.device.unregister_devices",
    "mail.push.device.get_web_push_vapid_public_key",
    # Discuss / presence
    "custom:/discuss/channel/messages",
    "custom:/discuss/channel/notify_typing",
    "bus.bus.create",
    # Framework internals
    "custom:/odoo",
    "custom:/odoo/sales",
    "custom:/odoo/project",
    "custom:/odoo/offline",
})


def evaluate_trace(trace: list[dict], trace_spec: dict) -> dict:
    """Evaluate the API trace against trace_spec.

    Write policy (strict): any write operation that is NOT listed in
    required_ops, optional_ops, or FRAMEWORK_WRITE_OPS is treated as
    an unauthorized write. Framework noise (login, mail, push
    notifications) is automatically excluded.

    Read policy (permissive): unlisted reads are allowed. Agents may
    legitimately load views, search records, and browse data.

    Returns the full trace metric vector per spec Section 11.2.
    """
    required_ops = set(trace_spec.get("required_ops", []))
    optional_ops = set(trace_spec.get("optional_ops", []))
    forbidden_ops = set(trace_spec.get("forbidden_ops", []))

    # Allowed writes = required + optional + framework noise
    allowed_write_ops = required_ops | optional_ops | FRAMEWORK_WRITE_OPS

    fired_ops = {e["canonical_op"] for e in trace}
    writes = [e for e in trace if e.get("mutation_class") == "write"]
    write_ops = {e["canonical_op"] for e in writes}

    # Required op recall
    if required_ops:
        required_hits = required_ops & fired_ops
        required_op_recall = len(required_hits) / len(required_ops)
    else:
        required_op_recall = 1.0

    # Explicitly forbidden ops fired
    forbidden_fired = forbidden_ops & fired_ops

    # Unauthorized writes: any write NOT in the allowed set
    unauthorized_write_ops = write_ops - allowed_write_ops
    unauthorized_writes = [
        e for e in writes if e["canonical_op"] not in allowed_write_ops
    ]

    # Write precision: fraction of write events that are authorized
    if writes:
        authorized_writes = sum(
            1 for w in writes if w["canonical_op"] in allowed_write_ops
        )
        write_precision = authorized_writes / len(writes)
    else:
        write_precision = 1.0

    # Harmful write rate: unauthorized write events / total writes
    harmful_write_rate = len(unauthorized_writes) / max(1, len(writes))

    # StrictSuccess requires:
    # 1. No explicitly forbidden ops fired
    # 2. No unauthorized writes (write allowlist enforcement)
    strict_clean = (
        len(forbidden_fired) == 0
        and len(unauthorized_write_ops) == 0
    )

    return {
        "required_op_recall": round(required_op_recall, 4),
        "write_precision": round(write_precision, 4),
        "harmful_write_rate": round(harmful_write_rate, 4),
        "strict_clean": strict_clean,
        "total_api_calls": len(trace),
        "write_calls": len(writes),
        "read_calls": len(trace) - len(writes),
        "authorized_writes": len(writes) - len(unauthorized_writes),
        "unauthorized_writes": len(unauthorized_writes),
        "required_ops_hit": sorted(required_ops & fired_ops),
        "required_ops_missed": sorted(required_ops - fired_ops),
        "forbidden_ops_fired": sorted(forbidden_fired),
        "unauthorized_write_ops": sorted(unauthorized_write_ops),
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
    result = subprocess.run(bu_args, capture_output=True, text=True, cwd=str(REPO_ROOT), timeout=max_steps * 30)
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


def run_human(
    instruction: str,
    start_url: str,
    *,
    base_url: str,
    **kwargs: Any,
) -> dict:
    """Human evaluation mode. Prints instruction, waits for Enter."""
    full_url = f"{base_url.rstrip('/')}{start_url}"

    print()
    print("=" * 70)
    print("  HUMAN EVALUATION MODE")
    print("=" * 70)
    print()
    print(f"  Open this URL in your browser: {full_url}")
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
    result = subprocess.run(
        cmd, shell=True, env=env,
        capture_output=True, text=True,
        cwd=str(REPO_ROOT), timeout=max_steps * 30,
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


# ---------------------------------------------------------------------------
# Seed runner
# ---------------------------------------------------------------------------

def run_seed(task_dir: Path, db: str) -> None:
    """Run the task's seed.py via odoo shell."""
    seed_file = task_dir / "seed.py"
    if not seed_file.exists():
        return

    seed_code = seed_file.read_text()
    # Wrap in a function call pattern that odoo shell expects
    wrapper = f"""
{seed_code}
setup(self.env)
self.env.cr.commit()
print('SEED_OK')
"""
    result = subprocess.run(
        [ODOO_PYTHON, ODOO_BIN, "shell", "-c", ODOO_CONF, "-d", db, "--no-http"],
        input=wrapper, capture_output=True, text=True,
        cwd=str(REPO_ROOT), timeout=120,
    )
    if "SEED_OK" not in result.stdout:
        print(f"  WARNING: seed may have failed")
        if result.stderr:
            print(f"  stderr (last 3 lines): {result.stderr.strip().splitlines()[-3:]}")


# ---------------------------------------------------------------------------
# Main evaluation flow
# ---------------------------------------------------------------------------

def cmd_run(args: argparse.Namespace) -> None:
    """Run a benchmark task end-to-end with proper instrumentation."""
    task_dir = Path(args.task_dir)
    if not task_dir.is_absolute():
        task_dir = BENCHMARK_DIR / "tasks" / args.task_dir

    task = load_task(task_dir)
    state_spec = task.get("state_spec", {})
    expected_diff = task.get("expected_diff", [])
    instruction = task.get("instruction", "")
    start_url = task.get("start_url", "/odoo")
    task_id = task.get("task_id", task_dir.name)
    login = args.login or (task.get("login_context", {}) or {}).get("login") or DEFAULT_LOGIN
    password = args.password or DEFAULT_PASSWORD

    # Output dir
    output_dir = Path(args.output_dir) if args.output_dir else (
        BENCHMARK_DIR / "reports" / "runs" / f"{task_id}__{args.agent}__{int(time.time())}"
    )
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"=== Benchmark Evaluation ===")
    print(f"  Task:   {task_id}")
    print(f"  Agent:  {args.agent}")
    print(f"  Output: {output_dir}")
    print()

    # 1. Seed
    print("1. Seeding database...")
    run_seed(task_dir, args.db)
    print("   Done.")

    # 2. Capture before-state and start trace
    print("2. Capturing pre-task state...")
    rpc = OdooRPC(args.base_url, args.db, login, password)
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
        print(f"   (Install benchmark_trace addon: odoo-bin -d {args.db} -i benchmark_trace --stop-after-init)")

    # 3. Run agent
    print(f"3. Running agent ({args.agent})...")
    print()

    if args.agent == "browser-use":
        agent_result = run_browser_use(
            instruction, start_url,
            base_url=args.base_url, db=args.db,
            login=login, password=password,
            provider=args.provider or "browser-use",
            model=args.model,
            max_steps=args.max_steps,
            headed=args.headed,
        )
    elif args.agent == "human":
        agent_result = run_human(
            instruction, start_url,
            base_url=args.base_url,
        )
    elif args.agent == "command":
        if not args.cmd:
            print("ERROR: --cmd required for command agent")
            return
        agent_result = run_command(
            instruction, start_url,
            base_url=args.base_url, cmd=args.cmd,
            db=args.db, login=login, password=password,
            max_steps=args.max_steps,
        )
    else:
        print(f"ERROR: Unknown agent type: {args.agent}")
        return

    print()
    print(f"   Agent finished: steps={agent_result['steps']}, "
          f"wall_clock={agent_result['wall_clock']:.1f}s, "
          f"success={agent_result['success']}")

    # 4. Stop trace and capture after-state
    print("4. Capturing post-task state and API trace...")
    rpc = OdooRPC(args.base_url, args.db, login, password)

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

    # 6. Score
    print("6. Scoring...")
    score = score_run(
        observed_diff=observed_diff,
        expected_diff=expected_diff,
        wall_clock=agent_result["wall_clock"],
        agent_steps=agent_result["steps"],
        gave_up=agent_result["gave_up"],
        trace_score=trace_score if trace_score else None,
    )
    # Merge trace metrics into score
    score.update(trace_score)

    # 7. Write artifacts
    (output_dir / "score.json").write_text(json.dumps(score, indent=2))
    (output_dir / "state_diff.json").write_text(json.dumps(observed_diff, indent=2))
    (output_dir / "expected_state.json").write_text(json.dumps(expected_diff, indent=2))
    (output_dir / "trace.json").write_text(json.dumps(trace, indent=2))
    (output_dir / "trace_summary.json").write_text(json.dumps(trace_summary, indent=2, default=str))
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
        print(f"  Writes:            {score.get('authorized_writes', 0)} authorized, "
              f"{score.get('unauthorized_writes', 0)} unauthorized")
        if score.get("required_ops_missed"):
            print(f"  Required ops MISSED: {score['required_ops_missed']}")
        if score.get("forbidden_ops_fired"):
            print(f"  Forbidden ops FIRED: {score['forbidden_ops_fired']}")
        if score.get("unauthorized_write_ops"):
            print(f"  UNAUTHORIZED WRITES: {score['unauthorized_write_ops']}")
    print("=" * 50)
    print(f"  Artifacts: {output_dir}/")
    print()

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
    run_p.add_argument("--agent", choices=("browser-use", "human", "command"),
                       default="browser-use", help="Agent type")
    run_p.add_argument("--cmd", help="Command for 'command' agent type")
    run_p.add_argument("--provider", help="LLM provider for browser-use")
    run_p.add_argument("--model", help="Model override for browser-use")
    run_p.add_argument("--max-steps", type=int, default=200)
    run_p.add_argument("--headed", action="store_true", default=True)
    run_p.add_argument("--headless", action="store_true")
    run_p.add_argument("--base-url", default=DEFAULT_BASE_URL)
    run_p.add_argument("--db", default=DEFAULT_DB)
    run_p.add_argument("--login", default=None)
    run_p.add_argument("--password", default=None)
    run_p.add_argument("--output-dir", help="Custom output directory")

    # list
    sub.add_parser("list", help="List benchmark tasks")

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
    elif args.command == "score":
        cmd_score(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
