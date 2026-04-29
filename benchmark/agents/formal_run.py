#!/usr/bin/env python3
"""Formal-run dispatcher for the /run-benchmark-agents skill.

Consumes the worker's claimed (agent, task) pairs from
`benchmark/reports/formal_run/queue.jsonl`, dispatches them at
`--parallel K`, captures token usage with a **per-run mitmdump proxy**
(so concurrent runs don't bleed tokens into each other), writes
artifacts under `formal_run/<agent>/<task>__<ts>/`, appends a `done`
row to the queue under an fcntl lock, and periodically commits+pushes
so other workers see progress.

Key behaviors encoded here (based on incidents in the first formal run):

- Pairs are interleaved by agent by default so the first K concurrent
  lanes each run a different agent. Running K copies of the same agent
  concentrates resource/rate-limit pressure in one place.
- Each run gets its own mitmdump proxy on a private free port + its
  own token log. Without this, time-window slicing of a shared proxy
  log attributes all concurrent runs' tokens to every one of them
  (observed directly in the first 8-pair pilot).
- After each run, kill any subprocess still carrying this run's unique
  `output_dir` in its argv — catches playwright/chromium/node/wrapper
  processes reparented to PID 1 when the `uv run` parent was reaped.
  The user's persistent Chrome (OpenBrowser) and unrelated processes
  are left alone.
- fcntl.flock for atomic queue.jsonl appends (macOS has no `flock` CLI).
- Commits happen every --commit-every completed runs, and on exit. If
  `git push` fails, retry once; otherwise log and keep going — we don't
  want a network blip to abort an 8-hour run.

Invocation example::

    python benchmark/agents/formal_run.py \\
        --worker xiao-1d1974 \\
        --parallel 4 \\
        --commit-every 10
"""
from __future__ import annotations

import argparse
import fcntl
import hashlib
import json
import os
import re
import socket
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
QUEUE_PATH = REPO_ROOT / "benchmark/reports/formal_run/queue.jsonl"
LOCK_PATH = REPO_ROOT / "benchmark/reports/formal_run/.queue.lock"
# Honor $BENCHMARK_SYSTEM_PY so each worker can point at the python
# where their agent packages (notte, skyvern, alumnium, websight) live.
# On xiao-cffef8 they're in miniforge3; on xiao-4dc953 they're in .venv.
SYSTEM_PY = os.environ.get(
    "BENCHMARK_SYSTEM_PY",
    str(REPO_ROOT / ".venv/bin/python3"),
)
MITMDUMP = "/Users/yangxiao/miniforge3/bin/mitmdump"
DASHSCOPE_UPSTREAM = "https://dashscope.aliyuncs.com"
OPENAI_UPSTREAM = "https://api.openai.com"
TOKEN_LOGGER_ADDON = "benchmark/agents/token_logger.py"

ACTIVE_AGENTS = [
    "browser-use", "notte", "skyvern", "alumnium",
    "magnitude", "agent_e", "openbrowser", "websight",
    "stagehand",
]

# Stagehand uses OpenAI gpt-4.1-mini directly; all other agents use Qwen via
# DashScope's OpenAI-compat endpoint. Each run gets its own reverse-proxy
# pointing at the right upstream so token_logger.py captures usage.
OPENAI_AGENTS = {"stagehand"}


def alloc_free_port() -> int:
    """Bind :0 to get a free ephemeral port from the kernel, then release."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def start_run_proxy(
    token_log: Path,
    stderr_log: Path,
    upstream: str = DASHSCOPE_UPSTREAM,
) -> tuple[int, subprocess.Popen]:
    """Start a per-run mitmdump and wait until it's accepting connections.

    Returns (port, Popen). Caller must terminate the Popen when the run
    is finished. Token log is truncated on start so it only holds this
    run's calls.
    """
    token_log.write_text("")
    port = alloc_free_port()
    with stderr_log.open("wb") as err:
        proc = subprocess.Popen(
            [
                MITMDUMP,
                "--mode", f"reverse:{upstream}",
                "-p", str(port),
                "--set", f"token_log={token_log}",
                "-s", str(REPO_ROOT / TOKEN_LOGGER_ADDON),
            ],
            cwd=str(REPO_ROOT),
            stdin=subprocess.DEVNULL,
            stdout=err, stderr=subprocess.STDOUT,
            close_fds=True,
            start_new_session=True,
        )
    # Poll the port until mitmdump binds (~0.3–1.5s in practice).
    for _ in range(100):
        if proc.poll() is not None:
            break
        try:
            with socket.create_connection(("127.0.0.1", port), timeout=0.1):
                return port, proc
        except OSError:
            time.sleep(0.1)
    proc.terminate()
    try:
        proc.wait(timeout=3)
    except subprocess.TimeoutExpired:
        proc.kill()
    raise RuntimeError(f"mitmdump failed to bind on {port}; see {stderr_log}")


def stop_run_proxy(proc: subprocess.Popen) -> None:
    if proc.poll() is not None:
        return
    proc.terminate()
    try:
        proc.wait(timeout=5)
    except subprocess.TimeoutExpired:
        proc.kill()


def load_queue() -> list[dict]:
    rows = []
    for line in QUEUE_PATH.read_text().splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return rows


def rewrite_queue(rows: list[dict]) -> None:
    with LOCK_PATH.open("w") as lk:
        fcntl.flock(lk.fileno(), fcntl.LOCK_EX)
        QUEUE_PATH.write_text("\n".join(json.dumps(r) for r in rows) + "\n")


def append_row(row: dict) -> None:
    with LOCK_PATH.open("w") as lk:
        fcntl.flock(lk.fileno(), fcntl.LOCK_EX)
        with QUEUE_PATH.open("a") as f:
            f.write(json.dumps(row) + "\n")


def pending_pairs_for(worker: str) -> list[tuple[str, str]]:
    """(agent, task) that the worker has claimed and not yet marked done."""
    rows = load_queue()
    claimed: set[tuple[str, str]] = set()
    done: set[tuple[str, str]] = set()
    for r in rows:
        # Defensive: skip malformed rows (our earlier dispatcher emitted some).
        a = r.get("agent", "")
        t = r.get("task", "")
        if not a or not t or " " in a:
            continue
        key = (a, t)
        if r.get("status") == "done":
            done.add(key)
        elif r.get("status") == "claimed" and r.get("worker") == worker:
            claimed.add(key)
    return sorted(claimed - done)


def interleave_by_agent(pairs: list[tuple[str, str]]) -> list[tuple[str, str]]:
    """[(bu, T0), (notte, T0), ..., (bu, T1), (notte, T1), ...] order.

    Ensures the first K lanes hit K distinct agents.
    """
    by_agent: dict[str, list[str]] = {a: [] for a in ACTIVE_AGENTS}
    for a, t in pairs:
        by_agent.setdefault(a, []).append(t)
    # Sort each agent's tasks alphabetically for determinism.
    for a in by_agent:
        by_agent[a].sort()
    out = []
    i = 0
    while True:
        added = False
        for a in ACTIVE_AGENTS:
            if i < len(by_agent.get(a, [])):
                out.append((a, by_agent[a][i]))
                added = True
        if not added:
            break
        i += 1
    return out


def short_db(agent: str, task: str) -> str:
    h = hashlib.md5(f"{agent}_{task}".encode()).hexdigest()[:8]
    return f"bench_fr_{h}"


def build_cmd(agent: str, task: str, db: str, outdir: Path, env: dict) -> list[str]:
    base = [
        "uv", "run", "benchmark-eval", "run", task,
        "--max-steps", "60", "--headed",
        "--db", db, "--output-dir", str(outdir),
    ]
    if agent == "browser-use":
        return base[:5] + [
            "--agent", "browser-use",
            "--provider", "dashscope", "--model", "qwen3.6-plus",
        ] + base[5:]
    if agent == "magnitude":
        # Magnitude needs strong visual grounding for pixel-coordinate clicks.
        # If ANTHROPIC_API_KEY is set, use Claude Sonnet 4.6 (Anthropic's
        # current recommended successor to Sonnet 4). Otherwise fall back
        # to qwen3.6-plus.
        anthropic_key = env.get("ANTHROPIC_API_KEY", "")
        if anthropic_key:
            model = env.get("BENCHMARK_MODEL", "claude-sonnet-4-6")
            inner = (
                f"ANTHROPIC_API_KEY={anthropic_key} "
                f"BENCHMARK_PROVIDER=anthropic "
                f"BENCHMARK_MODEL={model} BENCHMARK_MAX_STEPS=60 "
                f"node benchmark/agents/run_magnitude.mjs"
            )
        else:
            inner = (
                f"DASHSCOPE_API_KEY={env['DASHSCOPE_API_KEY']} "
                f"DASHSCOPE_BASE_URL={env['DASHSCOPE_BASE_URL']} "
                f"BENCHMARK_MODEL=qwen3.6-plus BENCHMARK_MAX_STEPS=60 "
                f"node benchmark/agents/run_magnitude.mjs"
            )
        return base[:5] + ["--agent", "command", "--cmd", inner] + base[5:]
    if agent == "stagehand":
        # Stagehand v3 + Qwen via DashScope is broken (see run_stagehand.mjs
        # comments). Use OpenAI gpt-4.1-mini through the per-run proxy.
        inner = (
            f"OPENAI_API_KEY={env['OPENAI_API_KEY']} "
            f"OPENAI_BASE_URL={env['OPENAI_BASE_URL']} "
            f"BENCHMARK_MODEL=gpt-4.1-mini BENCHMARK_MAX_STEPS=60 "
            f"node benchmark/agents/run_stagehand.mjs"
        )
        return base[:5] + ["--agent", "command", "--cmd", inner] + base[5:]
    # python wrappers
    wrapper = f"run_{agent}.py"
    inner = (
        f"DASHSCOPE_API_KEY={env['DASHSCOPE_API_KEY']} "
        f"DASHSCOPE_BASE_URL={env['DASHSCOPE_BASE_URL']} "
        f"OPENBROWSER_CHROME_UUID={env.get('OPENBROWSER_CHROME_UUID', '')} "
        f"BENCHMARK_MAX_STEPS=60 {SYSTEM_PY} benchmark/agents/{wrapper}"
    )
    return base[:5] + ["--agent", "command", "--cmd", inner] + base[5:]


def summarize_tokens(tokens_jsonl: Path, out: Path) -> dict:
    summary = {
        "requests": 0, "prompt_tokens": 0, "completion_tokens": 0,
        "total_tokens": 0, "reasoning_tokens": 0, "cached_tokens": 0,
    }
    if tokens_jsonl.exists():
        for line in tokens_jsonl.read_text().splitlines():
            if not line.strip():
                continue
            try:
                e = json.loads(line)
            except json.JSONDecodeError:
                continue
            summary["requests"] += 1
            for k in ("prompt_tokens", "completion_tokens", "total_tokens",
                      "reasoning_tokens", "cached_tokens"):
                summary[k] += e.get(k, 0) or 0
    out.write_text(json.dumps(summary, indent=2) + "\n")
    return summary


def find_run_processes(marker: str) -> list[int]:
    """Return PIDs whose command line contains `marker` (our run's unique
    output_dir string).

    This survives reparenting: even if the parent `uv run` process is
    reaped and children end up parented to PID 1, their command line
    still carries the --output-dir=<marker> arg (or the inner wrapper's
    BENCHMARK_* env vars exposed via -o args). We avoid killing any
    process that doesn't carry our marker — so the user's persistent
    Chrome (OpenBrowser), the human-mode eval, and unrelated tools are
    left alone.
    """
    try:
        out = subprocess.check_output(["ps", "-eo", "pid=,command="], text=True)
    except subprocess.CalledProcessError:
        return []
    pids = []
    for line in out.splitlines():
        line = line.strip()
        if not line or marker not in line:
            continue
        try:
            pids.append(int(line.split(None, 1)[0]))
        except ValueError:
            continue
    return pids


def kill_orphans(marker: str, keep_pid: int | None = None) -> int:
    """SIGTERM then SIGKILL any process carrying `marker` in its command
    line.

    `keep_pid` is the dispatcher's own PID (we don't want to kill
    ourselves if we ever carry the marker — e.g., we pass output_dir
    in our own argv).
    """
    pids = [p for p in find_run_processes(marker) if p != keep_pid]
    if not pids:
        return 0
    for pid in pids:
        try:
            os.kill(pid, 15)
        except (ProcessLookupError, PermissionError):
            pass
    time.sleep(1.0)
    killed = 0
    for pid in pids:
        try:
            os.kill(pid, 0)
            os.kill(pid, 9)
            killed += 1
        except (ProcessLookupError, PermissionError):
            # Process already exited from SIGTERM — that counts too.
            killed += 1
    return killed


# Chrome for Testing and related browser processes that agents launch.
# chrome_crashpad_handler in particular is deliberately detached (PPID=1
# from the moment it starts) so it survives a crashing browser and
# collects minidumps. That makes it invisible to any cleanup that walks
# from the subprocess tree, so we sweep for it explicitly.
_BROWSER_SIGNATURES = (
    "Chrome for Testing",
    "ms-playwright/chromium",
    "/temp/skyvern_browser_",
    "browser_use_local.py",
    "playwright/driver/node",
)


def reap_orphaned_browsers() -> int:
    """Kill any benchmark-browser process whose parent is PID 1.

    Safe to call between runs even with concurrent lanes: a process is
    only targeted if its parent is already gone (PPID==1), which can
    only be true for detached helpers (crashpad_handler) or for browsers
    whose launching agent already died. Legitimate in-flight lanes have
    their Chrome children parented to live wrappers.
    """
    try:
        out = subprocess.check_output(
            ["ps", "-eo", "pid=,ppid=,command="], text=True
        )
    except subprocess.CalledProcessError:
        return 0
    killed = 0
    import re as _re
    for line in out.splitlines():
        m = _re.match(r"\s*(\d+)\s+(\d+)\s+(.*)", line)
        if not m:
            continue
        pid, ppid, cmd = m.groups()
        if int(ppid) != 1:
            continue
        if not any(sig in cmd for sig in _BROWSER_SIGNATURES):
            continue
        try:
            os.kill(int(pid), 9)
            killed += 1
        except (ProcessLookupError, PermissionError):
            pass
    return killed


def run_one(agent: str, task: str, base_env: dict, worker: str) -> dict:
    ts = int(time.time())
    db = short_db(agent, task)
    outdir = REPO_ROOT / f"benchmark/reports/formal_run/{agent}/{task}__{ts}"
    outdir.mkdir(parents=True, exist_ok=True)
    # Don't use Path.with_suffix — the task folder name contains dots
    # (e.g. account.complete_customer_tax_id_then_post__<ts>) so
    # with_suffix rewrites the last dot-segment and produces `account.log`.
    log = outdir.parent / f"{outdir.name}.log"
    tokens_jsonl = outdir / "tokens.jsonl"

    # Per-run mitmdump so concurrent runs never share a token log.
    if agent in OPENAI_AGENTS:
        proxy_port, proxy_proc = start_run_proxy(
            tokens_jsonl, outdir / "mitm.log", upstream=OPENAI_UPSTREAM
        )
        env = {**base_env, "OPENAI_BASE_URL":
               f"http://127.0.0.1:{proxy_port}/v1"}
    else:
        proxy_port, proxy_proc = start_run_proxy(
            tokens_jsonl, outdir / "mitm.log"
        )
        env = {**base_env, "DASHSCOPE_BASE_URL":
               f"http://127.0.0.1:{proxy_port}/compatible-mode/v1"}
    cmd = build_cmd(agent, task, db, outdir, env)

    run_start = time.time()
    # Sanity check will be performed after the run: verify eval.py
    # printed "URL: http://127.0.0.1:<port>" with port != 8069. If it
    # didn't, auto-isolation failed and concurrent runs are sharing one
    # Odoo, which silently corrupts state capture + traces.
    try:
        with log.open("wb") as lf:
            proc = subprocess.Popen(
                cmd, cwd=str(REPO_ROOT),
                stdin=subprocess.DEVNULL,
                stdout=lf, stderr=subprocess.STDOUT,
                env={**os.environ, **env},
                close_fds=True,
                start_new_session=True,
            )
            try:
                rc = proc.wait(timeout=900)  # eval.py already caps at 600s; 900 is our hard outer bound
            except subprocess.TimeoutExpired:
                proc.terminate()
                try:
                    proc.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    proc.kill()
                rc = -1
        run_end = time.time()

        # Kill any subprocess that still carries our unique output_dir
        # marker in its command line. This catches playwright/chromium/
        # node/wrapper processes that got reparented to PID 1 when our
        # `uv run` parent was reaped — they're invisible to a ppid walk
        # but their argv still has `--output-dir=<outdir>`.
        killed = kill_orphans(str(outdir), keep_pid=os.getpid())
        # Chrome's crashpad_handler deliberately detaches with PPID=1
        # at launch, so marker-based cleanup misses it. Reap any
        # browser-family process whose parent is gone — harmless to
        # concurrent lanes since their browsers have live parents.
        killed += reap_orphaned_browsers()
    finally:
        stop_run_proxy(proxy_proc)

    token_summary = summarize_tokens(tokens_jsonl, outdir / "token_usage.json")

    # Parse score.
    score_path = outdir / "score.json"
    if score_path.exists():
        score = json.loads(score_path.read_text())
        verdict = "PASS" if score.get("strict_success") else "FAIL"
        f1 = score.get("state_diff_f1", 0.0)
        wall = score.get("wall_clock_sec", run_end - run_start)
    else:
        verdict = "ERROR"
        f1 = 0.0
        wall = run_end - run_start

    # Isolation sanity check. eval.py's auto-isolation must allocate a
    # free port per run — if it falls back to 8069, every concurrent run
    # shares one Odoo instance and all state captures / traces become
    # meaningless. This happened in the aborted first sweep: passing
    # --db disabled auto-isolation and every run landed on :8069.
    log_text = log.read_text(errors="replace") if log.exists() else ""
    url_match = re.search(r"URL:\s+http://127\.0\.0\.1:(\d+)", log_text)
    isolated_port = int(url_match.group(1)) if url_match else None
    if isolated_port is None or isolated_port == 8069:
        verdict = "ERROR"
        # Leave a breadcrumb in the row so the re-run loop knows these
        # shouldn't count.
        isolation_failed = True
    else:
        isolation_failed = False

    row = {
        "agent": agent, "task": task,
        "status": "done", "worker": worker,
        "ts": datetime.now(timezone.utc).isoformat(),
        "verdict": verdict, "f1": f1,
        "wall_clock": wall,
        "total_tokens": token_summary.get("total_tokens", 0),
        "output_dir": str(outdir.relative_to(REPO_ROOT)),
        "isolated_port": isolated_port,
        "isolation_failed": isolation_failed,
        "orphans_killed": killed,
        "rc": rc,
    }
    append_row(row)
    return row


def git_commit_push(worker: str, completed: int) -> None:
    """Stage the whole formal_run/ tree and push.

    Queue rows are authoritative for "what's done", but per-run artifacts
    (score.json, trace.json, trace_summary.json, tokens.jsonl, agent
    stdout/result, etc.) are needed for paper analysis — traces feed the
    required-ops / write-precision columns that the queue row only
    summarizes. Root .gitignore's `.*` keeps .worker_id and .queue.lock
    out.
    """
    try:
        subprocess.run(["git", "add", "benchmark/reports/formal_run/"],
                       check=True, cwd=str(REPO_ROOT))
        # Nothing to commit (e.g. artifacts all gitignored somehow, or
        # git_commit_push called back-to-back) is not an error.
        status = subprocess.run(
            ["git", "diff", "--cached", "--quiet"],
            cwd=str(REPO_ROOT),
        )
        if status.returncode == 0:
            return
        msg = f"formal_run: {worker} checkpoint ({completed} runs done)"
        subprocess.run(["git", "commit", "-m", msg], check=True, cwd=str(REPO_ROOT))
    except subprocess.CalledProcessError as e:
        print(f"[git] commit skipped: {e}", file=sys.stderr)
        return
    for attempt in (1, 2, 3):
        try:
            subprocess.run(["git", "push"], check=True, cwd=str(REPO_ROOT))
            return
        except subprocess.CalledProcessError as e:
            print(f"[git] push attempt {attempt} failed: {e}", file=sys.stderr)
            time.sleep(5 * attempt)


def list_tasks() -> list[str]:
    tasks_root = REPO_ROOT / "benchmark/tasks"
    return sorted(
        d.name for d in tasks_root.iterdir()
        if (d / "task.yaml").exists()
    )


def stream_claim(worker: str, n_tasks: int, agents: list[str] | None) -> int:
    """Claim (N tasks × chosen agents) with stream-safe git coordination.

    Protocol per attempt:
      1. reset local queue.jsonl to origin/<branch> (discarding any prior
         failed-claim commit) and pull the latest remote state
      2. recompute "unclaimed" = tasks not in any claimed/done row yet
      3. pick up to N unclaimed task slugs (FEWER if fewer remain)
      4. append (agent, task) claim rows for each (agents × N tasks)
      5. commit, push
      6. on push rejection: another worker beat us to pushing. "Give in"
         — hard-reset to remote, loop back to step 1. The next iteration
         will see the other worker's claims and pick DIFFERENT tasks
         from the freshly-shrunk unclaimed set. No retrying the same
         picks.
    """
    if agents is None:
        agents = ACTIVE_AGENTS
    all_tasks = list_tasks()

    branch = subprocess.run(
        ["git", "rev-parse", "--abbrev-ref", "HEAD"],
        capture_output=True, text=True, cwd=str(REPO_ROOT),
    ).stdout.strip()

    for attempt in range(1, 8):
        # 1. fetch + reset-hard to remote so queue.jsonl matches upstream.
        # On attempt > 1 this also discards our stale claim commit.
        subprocess.run(["git", "fetch", "origin"], check=False, cwd=str(REPO_ROOT))
        if attempt > 1:
            subprocess.run(
                ["git", "reset", "--hard", f"origin/{branch}"],
                check=False, cwd=str(REPO_ROOT),
            )
        else:
            # First attempt: preserve any unrelated local work; just rebase.
            rc = subprocess.run(
                ["git", "pull", "--rebase", "origin", branch],
                cwd=str(REPO_ROOT),
            )
            if rc.returncode != 0:
                print(f"[claim] attempt {attempt}: rebase failed; aborting",
                      file=sys.stderr)
                subprocess.run(["git", "rebase", "--abort"], cwd=str(REPO_ROOT))
                return 1

        # 2. compute what's taken from the fresh remote queue
        rows = load_queue()
        taken_by_agent: dict[str, set[str]] = {a: set() for a in agents}
        for r in rows:
            a = r.get("agent"); t = r.get("task")
            if not a or not t or a not in taken_by_agent:
                continue
            if r.get("status") in ("claimed", "done"):
                taken_by_agent[a].add(t)

        # 3. pick fresh unclaimed tasks (never re-pick from the prior attempt)
        unclaimed_tasks = [
            t for t in all_tasks
            if any(t not in taken_by_agent[a] for a in agents)
        ]
        if not unclaimed_tasks:
            print("[claim] nothing left to claim", file=sys.stderr)
            return 0

        picked = unclaimed_tasks[:n_tasks]
        now = datetime.now(timezone.utc).isoformat()

        # 4. write claim rows (skip any agent slot already taken)
        new_rows: list[dict] = []
        for t in picked:
            for a in agents:
                if t in taken_by_agent[a]:
                    continue
                new_rows.append({
                    "agent": a, "task": t,
                    "status": "claimed", "worker": worker, "ts": now,
                })
        if not new_rows:
            print("[claim] all agent×task slots already claimed",
                  file=sys.stderr)
            return 0

        with LOCK_PATH.open("w") as lk:
            fcntl.flock(lk.fileno(), fcntl.LOCK_EX)
            with QUEUE_PATH.open("a") as f:
                for r in new_rows:
                    f.write(json.dumps(r) + "\n")

        # 5. commit + push
        subprocess.run(["git", "add", "benchmark/reports/formal_run/queue.jsonl"],
                       check=True, cwd=str(REPO_ROOT))
        msg = (f"formal_run: {worker} claims {len(new_rows)} pairs "
               f"({len(picked)} tasks × {len(agents)} agents)")
        commit = subprocess.run(["git", "commit", "-m", msg], cwd=str(REPO_ROOT))
        if commit.returncode != 0:
            print("[claim] nothing to commit; already up to date",
                  file=sys.stderr)
            return 0
        push = subprocess.run(["git", "push"], cwd=str(REPO_ROOT))
        if push.returncode == 0:
            print(f"[claim] pushed {len(new_rows)} claims on attempt {attempt}",
                  file=sys.stderr)
            return 0

        # 6. push rejected — "give in", hard-reset to remote, and next
        # iteration picks fresh unclaimed tasks (never the same picks).
        print(f"[claim] attempt {attempt}: push rejected; giving up these "
              f"{len(picked)} task(s) and claiming new ones from the "
              f"post-rebase unclaimed set", file=sys.stderr)
        time.sleep(1.5 * attempt)

    print("[claim] exhausted retries", file=sys.stderr)
    return 1


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--worker", required=True)
    ap.add_argument("--parallel", type=int, default=1)
    ap.add_argument("--limit", type=int, default=0,
                    help="Only run this many pairs (0 = all pending)")
    ap.add_argument("--commit-every", type=int, default=10)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--claim", type=int, default=0,
                    help="Claim N tasks × agents (stream-safe: pull, append, "
                         "commit, push, rebase-retry on conflict), then exit")
    ap.add_argument("--agents", default=",".join(ACTIVE_AGENTS),
                    help="Comma-separated agent subset for --claim "
                         "(default: all 8 active agents)")
    args = ap.parse_args()

    if args.claim:
        agents = [a.strip() for a in args.agents.split(",") if a.strip()]
        return stream_claim(args.worker, args.claim, agents)

    dk = os.environ.get("DASHSCOPE_API_KEY")
    if not dk:
        print("DASHSCOPE_API_KEY not set", file=sys.stderr)
        return 1
    ok = os.environ.get("OPENAI_API_KEY")

    # Per-run proxies are spun up inside run_one, so we don't need an
    # externally-managed proxy anymore. We still pass DASHSCOPE_API_KEY
    # (and OPENAI_API_KEY for stagehand) via env; the *_BASE_URL is
    # overridden per-run.
    env = {
        "DASHSCOPE_API_KEY": dk,
        "OPENBROWSER_CHROME_UUID": os.environ.get("OPENBROWSER_CHROME_UUID", ""),
        # Optional: forward Anthropic key so run_magnitude.mjs can use Claude
        # for its pixel-coordinate visual grounding. Empty string means
        # qwen fallback path remains active.
        "ANTHROPIC_API_KEY": os.environ.get("ANTHROPIC_API_KEY", ""),
    }
    if ok:
        env["OPENAI_API_KEY"] = ok

    pending = pending_pairs_for(args.worker)
    pending = interleave_by_agent(pending)
    if args.limit:
        pending = pending[: args.limit]

    if any(a in OPENAI_AGENTS for a, _ in pending) and not ok:
        print("OPENAI_API_KEY required for stagehand pairs", file=sys.stderr)
        return 1

    print(f"worker={args.worker} K={args.parallel} pending={len(pending)}")
    for a, t in pending[:12]:
        print(f"  {a}\t{t}")
    if len(pending) > 12:
        print(f"  ... +{len(pending) - 12} more")

    if args.dry_run or not pending:
        return 0

    completed = 0
    with ThreadPoolExecutor(max_workers=args.parallel) as pool:
        futures = {pool.submit(run_one, a, t, env, args.worker): (a, t)
                   for a, t in pending}
        for fut in as_completed(futures):
            a, t = futures[fut]
            try:
                row = fut.result()
                print(f"[{a}|{t}] {row['verdict']} f1={row['f1']} "
                      f"wall={row['wall_clock']:.0f}s tokens={row['total_tokens']} "
                      f"orphans_killed={row['orphans_killed']}")
            except Exception as exc:  # noqa: BLE001
                print(f"[{a}|{t}] PYTHON ERROR: {exc}", file=sys.stderr)
            completed += 1
            if completed % args.commit_every == 0:
                git_commit_push(args.worker, completed)

    git_commit_push(args.worker, completed)
    return 0


if __name__ == "__main__":
    sys.exit(main())
