# Spec: Parallel Benchmark Evaluation

**Status:** Draft  
**Date:** 2026-04-14  
**Scope:** Enable concurrent execution of multiple `eval.py run` processes on a single machine

---

## 1. Problem

The current eval pipeline assumes it is the only `eval.py` process running. Running multiple `eval.py run <task>` commands concurrently — whether from separate terminals, a shell loop with `&`, or an external orchestrator — is broken.

Three hard blockers:

| Blocker | Location | Impact |
|---------|----------|--------|
| `pkill -f odoo-bin` | `eval.py:740` | Kills **every** Odoo process on the machine, including other eval runs |
| Shared database name | `--db benchmark_validate` | Concurrent restores corrupt each other's DB mid-episode |
| Single HTTP port | `.odoorc.local` → `http_port = 8069` | Two Odoo instances can't bind the same port |

The goal is: **any user should be able to open N terminals and run `eval.py run <task>` in each, with zero coordination between them.**

---

## 2. Design Principle: Self-Isolating Processes

There is no central orchestrator. Each `eval.py run` process is responsible for allocating its own isolated resources (DB, port, Odoo process) and cleaning them up when done. Processes don't know about each other — they just avoid collisions.

This is simpler and more composable than a pool/slot model. It works whether you launch tasks by hand, from `xargs -P`, from a Makefile, or from any CI system.

---

## 3. Design Goals

1. **Independent processes** — each `eval.py run` is fully self-contained; no shared state, no coordinator
2. **Automatic isolation** — each process gets its own DB, port, and Odoo server without manual flags
3. **Zero task definition changes** — `task.yaml`, `seed.py`, `prompt.md` etc. remain untouched
4. **Backward compatible** — existing `eval.py run <task> --db mydb --base-url ...` still works
5. **Deterministic cleanup** — resources cleaned up on normal exit, Ctrl-C, and crashes
6. **Stdlib only** — no external dependencies beyond what's already used

---

## 4. Per-Process Resource Allocation

### 4.1 Unique Run ID

Each `eval.py run` invocation generates a short unique ID at startup:

```python
import os, time
RUN_ID = f"{os.getpid()}_{int(time.time()) % 100000}"
# e.g. "48291_73845"
```

This ID namespaces all resources for the process.

### 4.2 Database Name

When the user does NOT pass an explicit `--db`:

```
benchmark_{task_id}_{RUN_ID}
```

Example: `benchmark_sale_confirm_correct_order_48291_73845`

When the user passes `--db mydb`, that name is used as-is (existing behavior, user takes responsibility for isolation).

### 4.3 Port Allocation

New flag `--port auto` (default when `--base-url` is not set):

```python
def find_free_port() -> int:
    """Bind to port 0, let the OS pick a free port, return it."""
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]
```

The allocated port is used for:
- Odoo `--http-port`
- XML-RPC connections (`OdooRPC(base_url=...)`)
- Agent `--base-url` / `BENCHMARK_BASE_URL`

When the user passes `--base-url http://...:8069`, auto-allocation is skipped (existing behavior).

### 4.4 Odoo Process — PID Tracking Instead of `pkill`

The fundamental fix. Replace the global `pkill -f odoo-bin` with tracked `subprocess.Popen`:

```python
class OdooProcess:
    """Manages a single Odoo server process for one eval run."""

    def __init__(self, db: str, port: int, conf: str, run_id: str):
        self.db = db
        self.port = port
        self.conf = conf
        self.run_id = run_id
        self._proc: subprocess.Popen | None = None
        self._log_path = Path(f"/tmp/bench_odoo_{run_id}.log")

    def start(self) -> None:
        self._proc = subprocess.Popen(
            [ODOO_PYTHON, ODOO_BIN,
             "-c", self.conf,
             "-d", self.db,
             "--http-port", str(self.port),
             "--no-database-list"],
            stdout=open(self._log_path, "w"),
            stderr=subprocess.STDOUT,
        )
        # Write PID file for crash recovery
        Path(f"/tmp/bench_odoo_{self.run_id}.pid").write_text(str(self._proc.pid))

    def stop(self) -> None:
        if self._proc and self._proc.poll() is None:
            self._proc.terminate()
            try:
                self._proc.wait(timeout=10)
            except subprocess.TimeoutExpired:
                self._proc.kill()
                self._proc.wait()
        # Clean up PID file
        pid_file = Path(f"/tmp/bench_odoo_{self.run_id}.pid")
        pid_file.unlink(missing_ok=True)

    def wait_ready(self, timeout: int = 60) -> None:
        """Poll HTTP until Odoo responds."""
        import urllib.request
        deadline = time.time() + timeout
        while time.time() < deadline:
            try:
                urllib.request.urlopen(
                    f"http://127.0.0.1:{self.port}/web/login", timeout=2
                )
                return
            except Exception:
                if self._proc.poll() is not None:
                    raise RuntimeError(
                        f"Odoo exited with code {self._proc.returncode}. "
                        f"See {self._log_path}"
                    )
                time.sleep(2)
        raise RuntimeError(f"Odoo not ready after {timeout}s on port {self.port}")
```

### 4.5 Per-Run Odoo Config

Each process writes a temporary config file derived from the base `.odoorc.local`:

```python
def _write_run_config(run_id: str, port: int, db: str) -> Path:
    import configparser
    config = configparser.ConfigParser()
    config.read(ODOO_CONF)
    config.set("options", "http_port", str(port))
    config.set("options", "db_name", db)

    path = Path(f"/tmp/bench_odoo_{run_id}.conf")
    with open(path, "w") as f:
        config.write(f)
    return path
```

Cleaned up alongside the process on exit.

---

## 5. Changes to `_prepare_episode`

This is the critical function. Replace global operations with process-scoped ones.

**Current flow:**
```
pkill -f odoo-bin          ← kills ALL Odoo everywhere
sleep(2)
restore DB                 ← to shared name "benchmark_validate"
clear asset cache
run seed
Popen(odoo-bin ...)        ← untracked process, default port
wait for ready
```

**New flow:**
```
odoo_proc.stop()           ← kills only THIS run's Odoo (by PID)
restore DB                 ← to unique name "benchmark_{task}_{run_id}"
clear asset cache
run seed                   ← using run-specific config
odoo_proc.start()          ← tracked process, unique port
odoo_proc.wait_ready()
```

```python
def _prepare_episode(
    db: str,
    task_dir: Path,
    base_url: str,
    *,
    snapshot_name: str | None = None,
    odoo_proc: OdooProcess | None = None,
) -> None:
    from benchmark.db import DatabaseManager
    dbm = DatabaseManager()
    restore_snapshot = snapshot_name or BASE_SNAPSHOT

    if restore_snapshot not in dbm.list_snapshots():
        if restore_snapshot == BASE_SNAPSHOT:
            _create_base_snapshot(db, dbm)
        else:
            raise RuntimeError(f"Snapshot '{restore_snapshot}' not found")

    # Stop THIS run's Odoo only
    if odoo_proc:
        odoo_proc.stop()
    else:
        # Legacy: no OdooProcess means old single-run behavior
        subprocess.run(["pkill", "-f", "odoo-bin"], capture_output=True)
        time.sleep(2)

    # Restore (unchanged — already parameterized by db name)
    dbm.restore_snapshot(restore_snapshot, db)

    # Clear asset cache (unchanged, uses db name)
    subprocess.run(
        ["psql", "-U", dbm.db_user, db, "-c",
         "DELETE FROM ir_attachment WHERE res_model='ir.ui.view' "
         "OR url LIKE '/web/assets/%';"],
        capture_output=True, env=dbm._pg_env(),
    )

    # Seed (unchanged)
    run_seed(task_dir, db)

    # Start THIS run's Odoo
    if odoo_proc:
        odoo_proc.start()
        odoo_proc.wait_ready()
    else:
        # Legacy
        subprocess.Popen(
            [ODOO_PYTHON, ODOO_BIN, "-c", ODOO_CONF, "-d", db],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
        # ... existing wait loop ...
```

---

## 6. Changes to `cmd_run`

### 6.1 Auto-Isolation Mode

When the user does not pass `--db` or `--base-url`, the run auto-isolates:

```python
def cmd_run(args: argparse.Namespace) -> dict | None:
    ...
    # Generate run ID
    run_id = f"{os.getpid()}_{int(time.time()) % 100000}"

    # Auto-isolate if no explicit DB/URL
    auto_isolate = (args.db == DEFAULT_DB and args.base_url == DEFAULT_BASE_URL
                    and not args.no_isolate)

    if auto_isolate:
        port = find_free_port()
        db = f"benchmark_{task_id}_{run_id}"
        base_url = f"http://127.0.0.1:{port}"
        conf_path = _write_run_config(run_id, port, db)
        odoo_proc = OdooProcess(db, port, str(conf_path), run_id)
    else:
        port = None  # use whatever --base-url says
        db = args.db
        base_url = args.base_url
        odoo_proc = None  # legacy mode

    try:
        _prepare_episode(db, task_dir, base_url,
                         snapshot_name=snapshot_name,
                         odoo_proc=odoo_proc)
        ...  # rest of evaluation (unchanged, but uses db/base_url vars)
    finally:
        if odoo_proc:
            odoo_proc.stop()
        if auto_isolate:
            _cleanup_run(run_id, db)
```

### 6.2 New CLI Flags

```
--no-isolate       Disable auto-isolation (use shared DB/port, old behavior)
--keep-db          Don't drop the per-run database after completion
--keep-server      Don't stop Odoo after completion (for debugging)
```

### 6.3 Return Score

`cmd_run` returns the score dict (in addition to printing it) so external callers can aggregate:

```python
def cmd_run(args) -> dict | None:
    ...
    return score
```

---

## 7. Cleanup

### 7.1 Normal Exit

In the `finally` block of `cmd_run`:

```python
def _cleanup_run(run_id: str, db: str) -> None:
    """Remove all per-run resources."""
    from benchmark.db import DatabaseManager

    # Drop ephemeral database
    try:
        DatabaseManager().drop_database(db)
    except Exception:
        pass  # best effort

    # Remove temp files
    for suffix in (".conf", ".pid", ".log"):
        Path(f"/tmp/bench_odoo_{run_id}{suffix}").unlink(missing_ok=True)
```

### 7.2 Signal Handling (Ctrl-C, SIGTERM)

Register cleanup on process signals so Ctrl-C doesn't leave orphans:

```python
import atexit, signal

_current_odoo_proc: OdooProcess | None = None
_current_run_id: str | None = None
_current_db: str | None = None

def _emergency_cleanup():
    if _current_odoo_proc:
        _current_odoo_proc.stop()
    if _current_run_id and _current_db:
        _cleanup_run(_current_run_id, _current_db)

atexit.register(_emergency_cleanup)
```

### 7.3 Crash Recovery — Stale PID Files

If a process crashes hard (SIGKILL), it may leave orphans. A simple `eval.py cleanup` subcommand:

```python
def cmd_cleanup(args):
    """Kill orphan benchmark Odoo processes and drop stale DBs."""
    # Find stale PID files
    for pid_file in Path("/tmp").glob("bench_odoo_*.pid"):
        pid = int(pid_file.read_text().strip())
        try:
            os.kill(pid, signal.SIGTERM)
            print(f"  Killed orphan Odoo (PID {pid})")
        except ProcessLookupError:
            pass
        pid_file.unlink()

    # Drop stale benchmark DBs
    dbm = DatabaseManager()
    result = subprocess.run(
        ["psql", "-tAc",
         "SELECT datname FROM pg_database WHERE datname LIKE 'benchmark_%_%'",
         "postgres"],
        capture_output=True, text=True, env=dbm._pg_env(),
    )
    for db_name in result.stdout.strip().splitlines():
        if db_name and db_name != "benchmark_validate":
            dbm.drop_database(db_name)
            print(f"  Dropped stale DB: {db_name}")
```

---

## 8. `run_seed` and `run_postconditions` — Config Propagation

Both functions shell out to `odoo-bin shell` with `-c ODOO_CONF`. In auto-isolate mode, they must use the per-run config so the shell connects to the right DB.

Change: pass `conf_path` as a parameter instead of using the global `ODOO_CONF`:

```python
def run_seed(task_dir: Path, db: str, conf_path: str = ODOO_CONF) -> None:
    ...
    result = subprocess.run(
        [ODOO_PYTHON, ODOO_BIN, "shell", "-c", conf_path, "-d", db, "--no-http"],
        ...
    )

def run_postconditions(task_dir: Path, db: str, conf_path: str = ODOO_CONF) -> list[str]:
    ...
    result = subprocess.run(
        [ODOO_PYTHON, ODOO_BIN, "shell", "-c", conf_path, "-d", db, "--no-http"],
        ...
    )
```

Default to `ODOO_CONF` so the single-run path is unchanged.

---

## 9. Filestore Isolation

Odoo stores files in `{data_dir}/filestore/{db_name}/`. Since each run has a unique DB name, filestores are naturally isolated. No changes needed.

Cleanup: `_cleanup_run` can optionally `shutil.rmtree` the filestore dir.

---

## 10. Example Usage

### 10.1 Single Run (unchanged)

```bash
uv run benchmark-eval run sale.confirm_correct_order --agent human
# Auto-isolates: own DB, own port, own Odoo process
```

### 10.2 Multiple Tasks in Parallel (terminals or background)

```bash
# Terminal 1
uv run benchmark-eval run sale.confirm_correct_order --agent browser-use

# Terminal 2 (simultaneously)
uv run benchmark-eval run project.read_update_status --agent browser-use

# Terminal 3 (simultaneously)
uv run benchmark-eval run crm.merge_duplicate_opportunities_cleanup --agent browser-use
```

Each gets its own DB and port. Zero coordination needed.

### 10.3 Shell Parallelism

```bash
# Run 4 tasks in parallel with xargs
echo "sale.confirm_correct_order
project.read_update_status
crm.merge_duplicate_opportunities_cleanup
calendar.schedule_recurring_steering_sync" | \
  xargs -P4 -I{} uv run benchmark-eval run {} --agent browser-use
```

### 10.4 All Tasks Parallel (updated run_all.sh)

```bash
# Updated run_all.sh uses xargs -P or GNU parallel
TASKS=$(uv run benchmark-eval list --ids-only)
echo "$TASKS" | xargs -P4 -I{} uv run benchmark-eval run {} --agent browser-use
```

### 10.5 Legacy Single-Port Mode

```bash
# Opt out of auto-isolation (old behavior)
uv run benchmark-eval run sale.confirm_correct_order --no-isolate
```

### 10.6 Cleanup Orphans

```bash
uv run benchmark-eval cleanup
```

---

## 11. Summary of Changes

| File | Change | Size |
|------|--------|------|
| `benchmark/eval.py` | Add `OdooProcess` class. Refactor `_prepare_episode` to accept it. Add auto-isolate logic to `cmd_run`. Add `cleanup` subcommand. Propagate `conf_path` through `run_seed`/`run_postconditions`. New CLI flags. | ~120 lines added, ~30 lines modified |
| `benchmark/run_all.sh` | Replace serial loop with `xargs -P` | ~10 lines changed |

**Files NOT changed:** `db.py`, `schema.py`, `metrics.py`, all task definitions, instrumentation modules, agent runners.

No new files. All changes in `eval.py`.

---

## 12. Risks & Mitigations

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| PostgreSQL `max_connections` hit with many Odoo instances | Medium | Each Odoo uses ~5 connections. 4 parallel = ~20. Default PG limit is 100. Document: `SHOW max_connections;` |
| Memory pressure (each Odoo ~200-400MB RSS) | Medium | 4 instances = ~1.6GB. User controls parallelism via how many they launch. |
| `find_free_port` race (port freed before Odoo binds) | Low | Extremely unlikely in practice. Odoo binds within ms. If it fails, the run errors cleanly. |
| Stale DBs accumulate if cleanup is skipped | Medium | `eval.py cleanup` command. DB names contain PID+timestamp so they're identifiable. |
| `seed.py` that does raw SQL with hardcoded DB names | Low | Audit: all current seeds use `self.env` (ORM context). ORM uses whatever DB the shell was started with. |
| Two runs of the same task read each other's before-state | None | Impossible — each has its own DB name. |

---

## 13. Implementation Checklist

1. Add `OdooProcess` class to `eval.py` (~40 lines)
2. Add `find_free_port()` and `_write_run_config()` helpers (~20 lines)
3. Add `_cleanup_run()` and `_emergency_cleanup()` + atexit registration (~25 lines)
4. Refactor `_prepare_episode` to accept `odoo_proc` parameter (~15 lines changed)
5. Add auto-isolate logic to `cmd_run` with try/finally cleanup (~30 lines)
6. Propagate `conf_path` param through `run_seed` and `run_postconditions` (~6 lines)
7. Add `--no-isolate`, `--keep-db`, `--keep-server` CLI flags (~10 lines)
8. Add `cleanup` subcommand (~20 lines)
9. Update `run_all.sh` to use `xargs -P` (~10 lines)
10. Test: run 2 tasks in separate terminals, verify isolation and cleanup
