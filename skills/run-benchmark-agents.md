---
name: run-benchmark-agents
description: Run the full benchmark suite for all browser agents against every task, coordinating multiple workers via a shared queue file in git. Each run records full artifacts (score, state diff, trace, stdout) plus per-run token consumption via a logging HTTP proxy. Use for formal evaluation runs.
user-invocable: true
argument-hint: "[--claim N] [--parallel K] [--agents a,b,...] [--continue]"
---

# Run Benchmark Agents — Formal Evaluation Runner

You are running the full benchmark suite — every task × every agent — for the
paper. This is the *production* eval path. Individual spot checks belong in
`validate-benchmark-tasks`.

Each run produces a full artifact directory (score, state diff, trace,
agent stdout) plus a `token_usage.json` capturing prompt/completion/reasoning
tokens consumed during that run. Multiple workers can share the load via a
git-coordinated queue file.

---

## Agents and model

The released runner includes Qwen/DashScope configurations, provider/model
variants, and Stagehand with OpenAI `gpt-4.1-mini`. See
`benchmark/agents/README.md` for current adapter configuration.

The manual orchestration examples below are historical development notes
for the Qwen campaign. For the maintained dispatcher and complete active-agent
set, inspect `benchmark/agents/formal_run.py --help` and its `ACTIVE_AGENTS`.
Stagehand and WebSight both have formal-run records covering all 424 tasks.

Adapters in the released repository:

| Agent | Runner |
|---|---|
| browser-use | `--agent browser-use --provider dashscope --model qwen3.6-plus` |
| notte | `python benchmark/agents/run_notte.py` |
| skyvern | `python benchmark/agents/run_skyvern.py` |
| alumnium | `python benchmark/agents/run_alumnium.py` |
| magnitude | `node benchmark/agents/run_magnitude.mjs` |
| agent_e | `python benchmark/agents/run_agent_e.py` |
| openbrowser | `python benchmark/agents/run_openbrowser.py` |
| websight | `python benchmark/agents/run_websight.py` |
| stagehand | `node benchmark/agents/run_stagehand.mjs` (OpenAI `gpt-4.1-mini`) |

Python wrappers must be invoked with the **system** python where the agent
package is installed, e.g. `python3`, **not**
`uv run python` (uv isolates its env and the agents aren't there).

---

## Coordination — shared queue

The queue is one JSONL file tracked in git:

```
benchmark/reports/formal_run/queue.jsonl
```

Each line is one **(agent, task)** run entry:

```jsonl
{"agent": "notte", "task": "sale.change_validity_date", "status": "claimed", "worker": "xiao", "ts": "2026-04-24T10:00:00"}
{"agent": "notte", "task": "crm.update_lead_email", "status": "done", "worker": "xiao", "ts": "2026-04-24T10:05:00", "verdict": "PASS", "f1": 1.0, "wall_clock": 265.8, "total_tokens": 17532, "output_dir": "benchmark/reports/formal_run/notte/crm.update_lead_email__1776938765"}
{"agent": "skyvern", "task": "calendar.create_single_event", "status": "done", "worker": "bob", "ts": "2026-04-24T10:07:00", "verdict": "FAIL", "f1": 0.0, "wall_clock": 600.0, "total_tokens": 41203, "output_dir": "..."}
```

### Statuses

- `claimed` — worker has reserved this (agent, task); other workers skip
- `done` — run finished; `verdict` is `PASS`/`FAIL`/`ERROR` plus metrics

### Workflow overview

0. Identify worker, start a token proxy, verify agent servers are up
1. Claim a batch of (agent, task) pairs
2. `git pull --rebase` to sync others' claims
3. Run each pair: invoke eval, record artifacts under `formal_run/<agent>/<task>__<ts>/`, append `done` row
4. Commit and push every 10 runs
5. Repeat until queue is empty

---

## Step 0 — Worker name and preflight

Per-machine worker ID. Same git user on multiple PCs would collide in the
queue; add a random suffix persisted locally so the same machine reuses its
ID across invocations. Store in `benchmark/reports/formal_run/.worker_id`
(ignored by the root `.gitignore`'s `.*` rule):

```bash
ID_FILE=benchmark/reports/formal_run/.worker_id
mkdir -p "$(dirname $ID_FILE)"
if [ ! -f "$ID_FILE" ]; then
  FIRST=$(git config user.name | awk '{print tolower($1)}')
  SUFFIX=$(python3 -c "import secrets; print(secrets.token_hex(3))")
  echo "${FIRST}-${SUFFIX}" > "$ID_FILE"
fi
worker=$(cat "$ID_FILE")   # e.g. "xiao-a1b2c3"
```

Claims and done rows will use this full ID, so queue entries from three of
your PCs look like `xiao-a1b2c3`, `xiao-d4e5f6`, `xiao-789abc` — no collisions.

### Preflight check — all must pass before claiming

```bash
# DashScope key
[ -n "$DASHSCOPE_API_KEY" ] || { echo "Missing DASHSCOPE_API_KEY"; exit 1; }

# Base snapshot exists
[ -f /tmp/benchmark_snapshots/benchmark_base.dump ] || { echo "Run 'uv run benchmark-eval prepare-base --db <seeded_db>' first"; exit 1; }

# Agent-E server up (skip if agent_e not in --agents)
curl -sS --max-time 3 http://127.0.0.1:8000/docs -o /dev/null

# OpenBrowser server up + Chrome UUID set (skip if openbrowser not in --agents)
[ -n "$OPENBROWSER_CHROME_UUID" ] || { echo "Missing OPENBROWSER_CHROME_UUID"; exit 1; }
curl -sS --max-time 3 http://127.0.0.1:8765/api | grep -q websocket_connected
```

---

## Step 1 — Start the token proxy

Token capture uses **mitmproxy** in reverse mode with a tiny logging addon
(`benchmark/agents/token_logger.py`). One-time install:

```bash
python3 -m pip install mitmproxy
```

One proxy per worker. Pick a free port to avoid collisions with sibling
workers on the same host:

```bash
PROXY_PORT=$((18000 + RANDOM % 1000))
PROXY_LOG_DIR=/tmp/token_logs_$worker
mkdir -p $PROXY_LOG_DIR
/Users/yangxiao/miniforge3/bin/mitmdump \
  --mode reverse:https://dashscope.aliyuncs.com \
  -p $PROXY_PORT \
  --set token_log=$PROXY_LOG_DIR/proxy.jsonl \
  -s benchmark/agents/token_logger.py \
  > $PROXY_LOG_DIR/mitm.log 2>&1 &
PROXY_PID=$!
sleep 2  # let mitmdump bind the port
```

For every agent invocation, point the DashScope base URL at the proxy.
**Keep the `/compatible-mode/v1` path suffix** — mitmproxy reverse mode
only rewrites the host, so clients must still send the real upstream path:

```bash
export DASHSCOPE_BASE_URL="http://127.0.0.1:$PROXY_PORT/compatible-mode/v1"
```

`_env_setup.py` (Python wrappers) and the Node wrappers all honor
`DASHSCOPE_BASE_URL`. `browser-use` picks it up via `browser_use_local.py`'s
`resolve_provider` path.

Important: do **not** pass `--set stream_large_bodies=...`. With streaming
enabled, `flow.response.content` is `None` in the `response()` hook and the
addon can't parse `usage`. The default (no streaming) is what you want.

### Agents whose tokens the proxy does NOT capture

- **Agent-E**: its long-running server has the upstream URL baked into
  `agents_llm_config.json`. To capture Agent-E tokens, stop the server and
  restart it with `model_base_url` pointed at `http://127.0.0.1:$PROXY_PORT`.
  Record `"agent_e_tokens": "uncaptured"` in the queue row if skipped.
- **OpenBrowser**: external server with its own upstream config. Same
  workaround as Agent-E if you want its tokens.

---

## Step 2 — Claim a batch

Parse `$ARGUMENTS`:
- `--claim N` — claim N pairs (default 20)
- `--agents a,b,c` — only claim for listed agents (default: all active 8)
- `--continue` — skip claiming; resume work on already-claimed rows for this
  worker that are not yet `done`
- `--parallel K` — run K pairs concurrently within this worker (default 1;
  see Parallelism caveats below)

To find unclaimed pairs:

```python
import json
from pathlib import Path
from datetime import datetime, timezone

ACTIVE_AGENTS = ["browser-use", "notte", "skyvern", "alumnium", "magnitude", "agent_e", "openbrowser", "websight"]

queue = Path("benchmark/reports/formal_run/queue.jsonl")
queue.parent.mkdir(parents=True, exist_ok=True)
queue.touch(exist_ok=True)

tasks = sorted(
    d.name for d in Path("benchmark/tasks").iterdir()
    if (d / "task.yaml").exists()
)

taken = set()
for line in queue.read_text().splitlines():
    if not line.strip():
        continue
    e = json.loads(line)
    taken.add((e["agent"], e["task"]))

want = [(a, t) for a in agents for t in tasks if (a, t) not in taken]
batch = want[: N]
```

Append `claimed` rows, commit, push:

```python
now = datetime.now(timezone.utc).isoformat()
with queue.open("a") as f:
    for a, t in batch:
        f.write(json.dumps({
            "agent": a, "task": t,
            "status": "claimed", "worker": worker, "ts": now,
        }) + "\n")
```

```bash
git add benchmark/reports/formal_run/queue.jsonl
git commit -m "formal_run: ${worker} claims ${N} pairs"
git push
```

Report what was claimed and how many pairs remain in the queue.

---

## Step 3 — Pull before each batch

```bash
git pull --rebase
```

If someone else raced a claim on one of ours, drop it and move on. The
JSONL is append-only, so "won" claims are the earliest rows for a given
(agent, task).

---

## Step 4 — Run each pair

### Output directory per run

```
benchmark/reports/formal_run/<agent>/<task>__<unix_ts>/
```

Keep `agent` and `task` in the path — aggregation scripts rely on this.

### Command construction

Per-agent command templates (all set `DASHSCOPE_BASE_URL` so the proxy sees
traffic). Use a short `--db` name (keep under 63 chars — PostgreSQL limit):

```bash
PY=python3
DB=$(python3 -c "import hashlib,sys; print('bench_fr_'+hashlib.md5(sys.argv[1].encode()).hexdigest()[:8])" "${agent}_${task}")
OUTDIR=benchmark/reports/formal_run/$agent/${task}__$(date +%s)
LOG=$OUTDIR.log
mkdir -p "$OUTDIR"

case "$agent" in
  browser-use)
    uv run benchmark-eval run "$task" \
      --agent browser-use --provider dashscope --model qwen3.6-plus \
      --max-steps 60 --headed \
      --db "$DB" --output-dir "$OUTDIR" > "$LOG" 2>&1 ;;
  notte|skyvern|alumnium|agent_e|openbrowser|websight)
    wrapper="run_${agent}.py"
    uv run benchmark-eval run "$task" \
      --agent command --cmd "DASHSCOPE_API_KEY=$DASHSCOPE_API_KEY DASHSCOPE_BASE_URL=$DASHSCOPE_BASE_URL OPENBROWSER_CHROME_UUID=$OPENBROWSER_CHROME_UUID BENCHMARK_MAX_STEPS=60 $PY benchmark/agents/$wrapper" \
      --max-steps 60 --headed \
      --db "$DB" --output-dir "$OUTDIR" > "$LOG" 2>&1 ;;
  magnitude)
    uv run benchmark-eval run "$task" \
      --agent command --cmd "DASHSCOPE_API_KEY=$DASHSCOPE_API_KEY DASHSCOPE_BASE_URL=$DASHSCOPE_BASE_URL BENCHMARK_MODEL=qwen3.6-plus BENCHMARK_MAX_STEPS=60 node benchmark/agents/run_magnitude.mjs" \
      --max-steps 60 --headed \
      --db "$DB" --output-dir "$OUTDIR" > "$LOG" 2>&1 ;;
esac
```

After the run, extract this run's slice of the proxy log and produce
`$OUTDIR/token_usage.json`. mitmproxy writes every call to one file
(`$PROXY_LOG_DIR/proxy.jsonl`) with a `ts` timestamp; filter by
`[RUN_START, RUN_END]`:

```bash
RUN_START=$(date +%s)    # capture before launching the agent
# ... run eval ...
RUN_END=$(date +%s)
# Slice and summarize
awk -v lo=$RUN_START -v hi=$RUN_END '
  {
    # match "ts": 1234567890.xxx
    if (match($0, /"ts"[[:space:]]*:[[:space:]]*[0-9.]+/)) {
      t = substr($0, RSTART, RLENGTH)
      gsub(/"ts"[[:space:]]*:[[:space:]]*/, "", t)
      if (t+0 >= lo && t+0 <= hi) print
    }
  }' "$PROXY_LOG_DIR/proxy.jsonl" > "$OUTDIR/tokens.jsonl"
python3 benchmark/agents/token_logger.py \
  summarize "$OUTDIR/tokens.jsonl" --out "$OUTDIR/token_usage.json"
```

Alternative (simpler, per-run precision): restart mitmdump between runs
pointed at a per-run log file. Costs ~1s start-up each but avoids the
timestamp slice.

### Parse the result

```bash
# eval.py writes JSON artifacts; just read score.json
F1=$(python3 -c "import json; print(json.load(open('$OUTDIR/score.json'))['state_diff_f1'])")
VERDICT=$(python3 -c "import json; d=json.load(open('$OUTDIR/score.json')); print('PASS' if d['strict_success'] else 'FAIL')")
WALL=$(python3 -c "import json; print(json.load(open('$OUTDIR/score.json'))['wall_clock_sec'])")
TOKENS=$(python3 -c "import json; print(json.load(open('$OUTDIR/token_usage.json'))['total_tokens'])")
```

If the run itself crashed (`eval.py` nonzero exit), record `verdict: ERROR`
with the log path for later triage.

### Append done row

```python
with queue.open("a") as f:
    f.write(json.dumps({
        "agent": agent, "task": task,
        "status": "done", "worker": worker, "ts": now,
        "verdict": verdict,             # PASS / FAIL / ERROR
        "f1": f1,
        "wall_clock": wall,
        "total_tokens": tokens,
        "output_dir": outdir,
    }) + "\n")
```

---

## Step 5 — Commit and push periodically

Every 10 completed runs (or after any ERROR verdict so colleagues can
triage):

```bash
git add benchmark/reports/formal_run/queue.jsonl
git commit -m "formal_run: ${worker} finished ${N} pairs (K pass)"
git push
```

Do **not** add `benchmark/reports/formal_run/<agent>/...` artifact
directories to git — they're too large. Gitignore them or keep on a
shared filesystem / object store. The queue JSONL has enough metadata
(f1, wall_clock, token counts, output_dir) for paper analysis.

---

## Parallel dispatch — implementing --parallel K

`--parallel K` governs how many (agent, task) pairs the worker runs
concurrently. It controls three things at once:

1. **Walltime per worker.** K=4 runs roughly 4× faster than K=1.
2. **DashScope rate-limit pressure.** Each concurrent run fires its own
   LLM calls. If the key has e.g. 120 req/min or 1M tokens/min, K=8 may
   saturate it and cause 429 errors. Lower K as needed.
3. **Trace correctness.** K>1 contaminates `trace.json`; see caveats below.

Implement the fan-out with `xargs -P K` over a pair-list file:

```bash
# Dump one claimed pair per line as "agent<TAB>task"
python3 - <<'PY' > /tmp/${worker}_pairs.tsv
import json
from pathlib import Path
q = Path("benchmark/reports/formal_run/queue.jsonl")
claimed = {}
done = set()
for line in q.read_text().splitlines():
    if not line.strip(): continue
    e = json.loads(line)
    key = (e["agent"], e["task"])
    if e["status"] == "done":
        done.add(key)
    elif e["status"] == "claimed" and e["worker"] == "${worker}":
        claimed[key] = e
for (a, t) in claimed:
    if (a, t) not in done:
        print(f"{a}\t{t}")
PY

# Fan out at parallelism K. Each child runs `run_one` on a single pair.
export DASHSCOPE_API_KEY DASHSCOPE_BASE_URL OPENBROWSER_CHROME_UUID worker
export -f run_one       # see Step 4 for the function body
cat /tmp/${worker}_pairs.tsv | \
  xargs -P "$K" -I{} bash -c 'IFS=$'"'"'\t'"'"' read -r a t <<< "{}"; run_one "$a" "$t"'
```

`run_one` does everything in Step 4 for one pair: allocate output dir,
construct the command, capture `RUN_START`/`RUN_END`, invoke eval, slice
proxy log, summarize tokens, append the `done` row. Make it serialize
writes to `queue.jsonl` with `flock` since multiple children append in
parallel:

```bash
run_one() {
  local agent="$1" task="$2"
  local ts=$(date +%s)
  local outdir="benchmark/reports/formal_run/$agent/${task}__$ts"
  mkdir -p "$outdir"
  local run_start=$(date +%s)
  # ... invoke eval.py per Step 4 ...
  local run_end=$(date +%s)
  # ... summarize tokens per Step 4 ...
  # Atomic append of the done row:
  (
    flock -x 200
    python3 -c "import json,sys; sys.stdout.write(json.dumps({\
      'agent':'$agent','task':'$task','status':'done','worker':'$worker',\
      'ts':'$(date -u +%FT%TZ)','verdict':'$verdict','f1':$f1,\
      'wall_clock':$wall,'total_tokens':$tokens,'output_dir':'$outdir'})+'\n')" \
      >> benchmark/reports/formal_run/queue.jsonl
  ) 200>benchmark/reports/formal_run/.queue.lock
}
```

### Rate-limit tuning

Start with **K=1** for the first handful of runs and watch the proxy log
for non-200 responses:

```bash
jq 'select(.status != 200) | {ts, status, path}' /tmp/token_logs_$worker/proxy.jsonl
```

If 429s appear, halve K. If nothing bad happens after 30 runs, double K
until either rate limits bite or wall-clock flatlines. Typical good
values on a single key: K=2-4.

A per-run slice already exists (`$OUTDIR/tokens.jsonl`); you can also
check the aggregate worker-wide usage against your DashScope quota:

```bash
python3 benchmark/agents/token_logger.py \
  summarize /tmp/token_logs_$worker/proxy.jsonl
```

---

## Parallelism caveats (READ BEFORE --parallel K)

`benchmark_trace` (the module that writes `trace.json`) currently records
to a shared log file within one Odoo host process group. When multiple
agent runs share a host, **the RPC trace is contaminated** — all runs get
byte-identical `trace.json` / `trace_summary.json`. The DB state and
`score.json` (f1, precision, recall, pass/fail, wall_clock) are per-run
correct, but these trace-derived metrics are not:

- `required_op_recall`
- `write_precision`
- `harmful_write_rate`
- `strict_clean`
- `total_api_calls`
- `write_calls`

### Two safe execution modes

1. **Serial per worker, many workers (recommended for paper-grade trace
   metrics).** `--parallel 1`. Multiple workers on different machines, or
   different worktrees, each with its own Odoo snapshot + token proxy.
   Trace is clean; wall-clock per worker scales linearly with task count.

2. **Parallel per worker, accept trace contamination.** `--parallel K`,
   one worker with K concurrent runs. Fine for smoke testing or F1-only
   analysis. Mark rows with `"trace_clean": false` when using this mode.

Until the trace module is fixed to namespace by DB or PID, either pick
(1) for formal numbers or disclose (2) in the paper methodology.

---

## Summary report

After the queue is drained, generate a summary:

```
benchmark/reports/formal_run/summary_YYYYMMDD.md
```

```python
from collections import defaultdict
from pathlib import Path
import json

rows = [json.loads(l) for l in Path("benchmark/reports/formal_run/queue.jsonl").read_text().splitlines() if l.strip()]
done = [r for r in rows if r.get("status") == "done"]

by_agent = defaultdict(list)
for r in done:
    by_agent[r["agent"]].append(r)

lines = ["# Formal Run Summary\n"]
lines.append(f"Total (agent, task) pairs: {len(done)}\n")
lines.append("| Agent | N | Pass | Fail | Error | Mean F1 | Mean wall | Mean tokens |")
lines.append("|---|---:|---:|---:|---:|---:|---:|---:|")
for agent, rs in sorted(by_agent.items()):
    n = len(rs)
    p = sum(1 for r in rs if r.get("verdict") == "PASS")
    f = sum(1 for r in rs if r.get("verdict") == "FAIL")
    e = sum(1 for r in rs if r.get("verdict") == "ERROR")
    mf1 = sum(r.get("f1", 0) for r in rs) / max(n, 1)
    mw = sum(r.get("wall_clock", 0) for r in rs) / max(n, 1)
    mt = sum(r.get("total_tokens", 0) for r in rs) / max(n, 1)
    lines.append(f"| {agent} | {n} | {p} | {f} | {e} | {mf1:.2f} | {mw:.0f}s | {mt:,.0f} |")
```

---

## Troubleshooting

- **`ModuleNotFoundError: No module named 'notte'`** — you invoked the
  wrapper through `uv run python`; use the system python path directly.
- **`createdb` fails with name too long** — the skill's `$DB` formula
  keeps names to `bench_fr_<8-hex>` (17 chars). Don't extend it.
- **Proxy not logging** — several possibilities:
  - Agent is hitting the real DashScope host. Verify `echo $DASHSCOPE_BASE_URL`
    inside `--cmd` propagates through eval.py's env passing.
  - Base URL is missing the `/compatible-mode/v1` suffix. mitmproxy reverse
    mode only rewrites the host; clients must send the full upstream path.
  - mitmdump logs show `(content missing)` — streaming is enabled. Remove
    any `--set stream_large_bodies=...` flag.
  - Check addon errors: `tail $PROXY_LOG_DIR/mitm.log`.
- **Agent-E tokens always 0** — its long-running server wasn't restarted
  against the proxy. See "Agents whose tokens the proxy does NOT capture"
  above.
- **Identical `trace.json` across agents** — you're running with
  `--parallel K > 1`. Expected; see Parallelism caveats.
