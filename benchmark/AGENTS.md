# AGENTS.md — Benchmark Setup for AI Agents

Terse, decision-oriented reference for an AI coding agent landing in this
repo cold. If you're here to **run the benchmark**, start at `§ Run a
verification task`. If you're here to **bootstrap a new machine**, work top
to bottom.

---

## What this is

Browser-agent benchmark layered on a real Odoo 19 instance. Each task seeds
a draft-quote / PO / lead / etc., the agent drives the web UI, and scoring
compares DB state + RPC trace against an oracle. Harness entry point:
`uv run benchmark-eval`. Active evaluation is against **qwen3.6-plus** via
DashScope's OpenAI-compatible endpoint.

Layout:

```
benchmark/
  AGENTS.md              ← you are here
  eval.py, db.py, ...    ← harness
  tasks/<task>/          ← 424 tasks; each has prompt.md + seed.py + check.py + oracle.py
  agents/                ← one wrapper per browser-agent framework
    setup.sh             ← dependency installer (Python + Node + Agent-E)
    token_logger.py      ← mitmproxy addon that captures LLM usage per run
    README.md            ← per-agent install notes, test results, troubleshooting
  reports/
    formal_run/          ← outputs + queue.jsonl for the distributed run
    ...                  ← previous run corpora (human_eval, difficulty_tests, ...)
skills/
  run-benchmark-agents.md  ← distributed formal-run skill (JSONL queue, mitmproxy, worker IDs)
  validate-benchmark-tasks.md
  create-benchmark-task.md
  ...
```

---

## Prerequisites (binary check)

| Requirement | Check |
|---|---|
| Python 3.11+ | `python3 --version` |
| Node 18+ | `node --version` |
| PostgreSQL 14+, running locally | `psql -l` |
| `uv` | `uv --version` |
| `git` | `git --version` |
| Chrome (for OpenBrowser) | optional; skip if not using that agent |

If `uv` is missing: `curl -LsSf https://astral.sh/uv/install.sh | sh`.

---

## One-time setup

### 1. Install the Odoo venv

The harness calls `odoo-bin` through `.venv/bin/python3`. Create it once:

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt   # or setup/requirements-check.py
```

### 2. Write `.odoorc.local`

File lives at repo root; `eval.py` reads it for the Postgres user and addons
path. Minimum content:

```ini
[options]
addons_path = <repo>/addons,<repo>/odoo/addons
db_user = <your-postgres-user>
http_interface = 127.0.0.1
http_port = 8069
data_dir = <repo>/.odoo-data
without_demo = True
```

### 3. Install the benchmark package + agent deps

```bash
uv sync                              # installs `benchmark-eval` entrypoint
cd benchmark/agents && bash setup.sh # installs Python + Node agents, Agent-E clone
```

`setup.sh` installs: `skyvern`, `notte`, `websight`, `alumnium`,
`langchain-openai`, Playwright chromium, `@browserbasehq/stagehand`,
`magnitude-core`, `mitmproxy`, and clones Agent-E into
`benchmark/agents/vendor/Agent-E/` with its own venv (Agent-E's pinned
`pydantic==2.6.2` conflicts with the other agents).

### 4. Build the base DB snapshot

All task runs restore from `/tmp/benchmark_snapshots/benchmark_base.dump`.
Build it once:

```bash
uv run benchmark-eval bootstrap-base
# or if you already have a DB with the needed modules:
uv run benchmark-eval prepare-base --db <your-seeded-db>
```

`bootstrap-base` reads `benchmark/base_modules.txt` (root modules only —
transitive deps are pulled in by Odoo) and installs into a fresh DB.

### 5. External agent servers (optional, per agent)

These aren't auto-started by `setup.sh`. Skip if the agent isn't in your
run set.

**Agent-E** — needs its own long-running server on port 8000:

```bash
cd benchmark/agents/vendor/Agent-E
PYTHONPATH=. .venv/bin/python3 -c "
import nest_asyncio; nest_asyncio.apply()
import asyncio; asyncio.set_event_loop_policy(None)
from ae.server.api_routes import app
import uvicorn
uvicorn.run(app, host='0.0.0.0', port=8000, loop='asyncio')
"
```

Also edit `vendor/Agent-E/agents_llm_config.json` so both of its model
slots point at qwen3.6-plus via DashScope before starting the server.

**OpenBrowser** — external server + Chrome extension. Not auto-installable:

1. Clone `github.com/softpudding/OpenBrowser` somewhere.
2. Start server: `cd OpenBrowser/server && python main.py start` (port 8765).
3. Install the Chrome extension from the repo, open Chrome, connect.
4. Copy the browser UUID printed by the extension into your shell:
   `export OPENBROWSER_CHROME_UUID=<uuid>`.

---

## Environment variables

```bash
export DASHSCOPE_API_KEY=sk-...          # required by every agent
export OPENBROWSER_CHROME_UUID=...       # only if running OpenBrowser
# Optional:
export BENCHMARK_MODEL=qwen3.6-plus      # default already qwen3.6-plus
export DASHSCOPE_BASE_URL=https://...    # set by run-benchmark-agents skill
                                         # to point at the mitmproxy
```

---

## Run a verification task

Smoke test the whole pipeline against the easy
`sale.change_validity_date` task with browser-use:

```bash
uv run benchmark-eval run sale.change_validity_date \
  --agent browser-use --provider dashscope --model qwen3.6-plus \
  --max-steps 60 --headed \
  --db bench_smoke \
  --output-dir /tmp/smoke_browser_use
```

Expected: `RESULT: PASS`, `StateDiffF1: 1.0`, wall clock ~250–350s.

If this works, the rest of the pipeline is wired correctly.

---

## Formal eval batch

Use the skill `skills/run-benchmark-agents.md`. It handles distributed
workers via a git-coordinated JSONL queue at
`benchmark/reports/formal_run/queue.jsonl`, per-machine worker IDs,
mitmproxy-based token logging, `--parallel K` fan-out with `xargs -P` +
`flock`, and per-run artifact dirs (score/state-diff/trace/stdout plus
`token_usage.json`). Read its header before first use.

---

## Common pitfalls

- **`ModuleNotFoundError: No module named 'notte'`** — you invoked the
  wrapper via `uv run python`. `uv` isolates its env and the agents live
  in the system Python (`/Users/.../miniforge3/bin/python3` on mac,
  whatever `which python3` points at elsewhere). Always invoke agent
  wrappers with that absolute path.
- **`createdb: database name too long`** — Postgres caps at 63 chars.
  The skill derives short DB names (`bench_fr_<8hex>`); don't extend.
- **Task fails instantly with `Snapshot not found`** — you skipped step 4.
- **Parallel `trace.json` files are byte-identical** — benchmark_trace
  currently writes to a shared log per host. Run serially per worker, or
  accept contaminated RPC metrics; see the skill's Parallelism caveats.
- **Stagehand dies with "Invalid JSON response"** — known DashScope
  server-side bug (`MMGPT3Item not JSON serializable` on multi-turn tool
  calls via the Responses API). Stagehand is excluded from current runs;
  see `benchmark/agents/README.md` for the writeup.
- **`.worker_id` missing** — the formal-run skill auto-generates it on
  first run. It lives at `benchmark/reports/formal_run/.worker_id` and is
  covered by the root `.gitignore`'s `.*` rule.

---

## Quick commands

```bash
# List all tasks
uv run benchmark-eval list

# Run one task against one agent (human mode for manual walkthrough)
uv run benchmark-eval run <task> --agent human

# Re-score an existing output dir
uv run benchmark-eval score <output_dir> --task <task_dir>

# Kill stale benchmark Odoo processes / drop ephemeral DBs
uv run benchmark-eval cleanup

# Aggregate token usage across a worker's proxy log
/Users/yangxiao/miniforge3/bin/python3 benchmark/agents/token_logger.py \
  summarize /tmp/token_logs_<worker>/proxy.jsonl
```
