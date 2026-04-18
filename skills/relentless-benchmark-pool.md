---
name: relentless-benchmark-pool
description: Continuously and relentlessly produce new benchmark tasks using a rolling pool of N parallel worktree agents. Encodes lessons from prior batches: pre-warmed worktrees, single-shot browser-use, agent-owned STATUS rows, pre-generated backlog, and an Odoo 19 cookbook. Use when the user wants sustained throughput (e.g. "build 50 tasks", "run rolling-8 until backlog empty", "keep going until I stop you").
user-invocable: true
argument-hint: [pool_size]:[stop_condition] — e.g. "8:50tasks" or "5:until-backlog-empty" or "10:60min". Blank defaults to 5:until-backlog-empty.
---

# Relentless Benchmark Pool

Run a sustained rolling pool of N parallel benchmark-task builder agents. As each
agent completes, immediately launch a replacement from a pre-generated backlog —
keeping N agents in flight at all times until a stop condition is met.

This is the **production mode** for benchmark expansion. Use after the gap-finding
and design phase is settled and the goal is *throughput*.

---

## Why this skill exists

Across the first two batches of 10-each, several recurring inefficiencies were
empirically identified:

1. Each agent re-installed the worktree venv (1–3 min × every agent)
2. Parallel `pkill -f odoo-bin` and `cleanup` killed sibling Odoo processes
3. Each task ran browser-use twice, even when run 1 was decisive
4. Per-batch coverage re-scan + ideation took ~30 min of orchestrator time
5. Each agent rediscovered Odoo 19 quirks (button labels, hidden tabs)
6. Snapshot occasionally lacked modules listed in `base_modules.txt`
7. Orchestrator manually cherry-picked + edited STATUS.md on every batch

This skill encodes the fixes for all seven.

---

## Inputs

Parse `$ARGUMENTS` as `[pool_size]:[stop_condition]`. Defaults if unspecified:
- `pool_size = 5`
- `stop_condition = until-backlog-empty`

Stop condition syntax:
- `<N>tasks` — stop after N tasks have been completed (not started)
- `<N>min` — stop after N wall-clock minutes
- `until-backlog-empty` — stop when no more pending entries remain in the backlog
- `until-stop` — never stop on your own; require an explicit user message

`pool_size` should be 4–8 in practice. Below 4 wastes parallelism; above 8
re-introduces the resource contention we just optimized away.

---

## Phase 0 — Infrastructure preflight (one-time, ~5 min)

These checks are **idempotent**. If a fix is already in place, skip it.

### 0.1 — Cleanup-collision patch

Check that `benchmark/eval.py` cleanup logic is **scoped to the current
worktree's PID/DB only**, not globbing every `benchmark_*` DB or every
`odoo-bin` process on the host.

```bash
grep -nE "pkill -f odoo-bin|benchmark_\*|cleanup_all" benchmark/eval.py | head -20
```

If you find an unscoped `pkill -f odoo-bin` or wildcard `benchmark_*` cleanup,
**stop the skill** and tell the user: "Infra patch needed before relentless
mode is safe — sibling worktrees will kill each other. Recommend fixing first
(I can do it as a one-shot agent, ~30 min)."

### 0.2 — Pre-warmed worktree skeleton

Check for a reusable skeleton:

```bash
ls .claude/worktree-skeleton/.venv/bin/python 2>/dev/null && \
  ls .claude/worktree-skeleton/.odoorc.local 2>/dev/null
```

If missing, build it once with these commands (run in main repo, NOT in a
worktree):

```bash
mkdir -p .claude/worktree-skeleton
cp .odoorc.local .claude/worktree-skeleton/.odoorc.local
uv venv .claude/worktree-skeleton/.venv
.claude/worktree-skeleton/.venv/bin/pip install -r requirements.txt
.claude/worktree-skeleton/.venv/bin/pip install browser-use playwright babel passlib
.claude/worktree-skeleton/.venv/bin/playwright install chromium
```

Agents will then symlink/copy from this skeleton instead of re-installing.

### 0.3 — Snapshot completeness

Verify the base snapshot has every module from `base_modules.txt` actually
installed. The previous batches saw `survey` and `maintenance` listed but
uninstalled in the snapshot, forcing per-agent `button_immediate_install`.

```bash
psql -tAc "SELECT name FROM ir_module_module WHERE state='uninstalled' AND name IN ($(awk 'NF && !/^#/ {printf "\"%s\",", $1}' benchmark/base_modules.txt | sed 's/,$//'))" benchmark_validate
```

If the result is non-empty, run:

```bash
.venv/bin/python odoo-bin -d benchmark_validate -i $(paste -sd, benchmark/base_modules.txt) -c .odoorc.local --stop-after-init
PYTHONPATH=. .venv/bin/python benchmark/eval.py prepare-base --db benchmark_validate
```

### 0.4 — Postgres connection limit

```bash
psql -tAc "SHOW max_connections" postgres
```

If < 200, advise the user to bump it (`max_connections = 200` in
`postgresql.conf` + restart). Don't block on this — it's a soft constraint.

### 0.5 — Odoo 19 cookbook

Check for `benchmark/ODOO19_PATTERNS.md`. If missing, write a stub with these
**empirically discovered** quirks (each was rediscovered by 1–3 agents):

```markdown
# Odoo 19 patterns and gotchas — for benchmark task builders

## Module names that changed
- `service_policy='delivered_timesheet'` requires `sale_timesheet` (NOT in base snapshot)
- `service_policy='delivered_milestones'` works with `sale_project` + `project.milestone`
- Replenishment lives at `/odoo/replenishment` (server action), under
  Inventory → Operations → Procurement → Replenishment

## Field name surprises
- `tax_ids` not `tax_id` on sale.order.line
- `group_ids` not `groups_id` on res.users
- `memo` not `ref` on account.payment
- `product_qty` not `quantity` on purchase.order.line
- `slide.question.question` (Char) not `name`/`title`
- `slide.answer.text_value` not `value`/`name`
- `mailing_model_name` on mailing.mailing must be set; `mailing_model_id` alone is insufficient
- `email_from` is required by DB constraint on mailing.mailing — set it on JSON-RPC create
- `fleet.vehicle.write` auto-creates a `fleet.vehicle.assignation.log` entry on driver_id change
- `maintenance.equipment.period` was removed in Odoo 19; use `expected_mtbf` instead
- `mtbf` is computed/readonly; `expected_mtbf` is writable

## UI navigation surprises
- `is_published` boolean on website_sale products is the Sales-tab toggle, NOT the form-header `website_redirect_button`
- Recruitment kanban "New" opens a stub modal; full job form needs "Configure" on the kanban card
- Live Chat kanban opens the chat session, not the form — use 3-dots → "Configure Channel"
- Survey form hides Time Limit field when `survey_type='survey'`; use `'custom'` to expose it
- Webshop Products list defaults to kanban with `search_default_published=1` — must clear filter for archived
- Public-portal apply form for jobs requires LinkedIn OR Resume (client-side JS validation)
- Backorder dialog: "Create Backorder" is the default/primary button in Odoo 19

## Patterns
- For datetime fields with admin TZ, use `ignore_fields: [date_deadline]` in state_spec.yaml
  and verify via `check.py` after timezone normalization (see project_todo.reorder_notes_add_due_dates_bulk)
- For modules that may be uninstalled in the snapshot, call `button_immediate_install()` in seed.py
  (see survey.create_feedback_survey_with_sections/seed.py)
- For fragile UI navigation (filters, complex tabs), oracle.py may use JSON-RPC `call_kw` to
  set canonical state; the agent must still solve via UI
- The diff engine emits `is_correct=null` (not `False`) for unchecked Booleans — match in expected_state.json
```

Add to this file as future agents discover new quirks. **Every builder agent
must read it before writing code.**

---

## Phase 1 — Backlog generation (~30 min, one-time per session)

The backlog lives at `.claude/relentless-pool/backlog.jsonl`. Each line is a
JSON object with the full task spec.

### 1.1 — Re-scan coverage

Run the same analysis as `expand-benchmark-coverage`:
- Count `Done`+`WIP` rows per module
- Identify zero-coverage installed modules
- Identify low-coverage (1–3 tasks) modules
- Cross-check WIPs to avoid duplicates

### 1.2 — Generate ≥ 30 task specs

Brainstorm task ideas covering:
- All zero-coverage installed modules first (highest value)
- All low-coverage modules with at least one underexploited workflow
- Variants on existing modules using **proven hard patterns**:
  - Wizard with non-default radio
  - Inline-cell edit that's hard to persist
  - Multi-step kanban modal (stub-form → Configure)
  - Cross-module smart-button chain (kept implicit, no explicit hints)
  - File upload widget
  - Settings-tab Many2one
  - Datetime field requiring exact value (avoid "today coincidence" — use a date ≥ 30 days from current)
  - Domain filter wizard

For each spec, write a JSON line with these fields:

```json
{
  "row": 294,
  "task_id": "module.descriptive_name",
  "difficulty": "medium",
  "tier": 2,
  "time_limit_sec": 360,
  "step_limit": 200,
  "summary": "one-line description for STATUS.md",
  "modules": ["module1", "module2"],
  "workflow": "2-3 sentences describing the agent's actions in concrete terms",
  "hard_pattern": "which proven failure pattern this exercises",
  "reference_tasks": ["benchmark/tasks/foo.bar/", "benchmark/tasks/baz.qux/"],
  "distinct_from": "1-line: how this differs from existing+WIP tasks in the same module",
  "check_focus": "what check.py asserts (key invariants)",
  "calibration_risk": "what makes this match its tier; what would make it too easy"
}
```

Pre-allocate sequential row numbers starting from `(max_row_in_STATUS.md + 1)`.

### 1.3 — Reserve all rows in one commit

Add WIP rows to `benchmark/tasks/STATUS.md` for every backlog entry, commit,
push:

```bash
git add benchmark/tasks/STATUS.md
git commit -m "[WIP] benchmark: reserve N relentless-pool tasks (rows X–Y)"
git pull --rebase origin odoo_benchmark
git push origin odoo_benchmark
```

This single up-front reservation is critical — agents commit only their own
task directory and **own STATUS row**, so they never collide.

---

## Phase 2 — Pool execution (rolling)

Maintain state in `.claude/relentless-pool/manifest.json`:

```json
{
  "pool_size": 5,
  "started_at": "2026-04-18T12:30:00Z",
  "stop_condition": "until-backlog-empty",
  "completed": [{"row": 294, "agent_id": "...", "commit": "...", "result": "..."}],
  "in_flight": [{"row": 295, "agent_id": "...", "launched_at": "..."}],
  "pending_rows": [296, 297, 298, ...]
}
```

### 2.1 — Initial fan-out

Launch the first `pool_size` agents in parallel, each picking the next pending
row. Each agent gets the **standardized prompt template** below.

### 2.2 — Standardized agent prompt template

Use this exact structure (substitute `{{ ... }}` from the backlog entry):

```
You are building benchmark task `{{task_id}}` (difficulty: **{{difficulty}}**) for the Odoo browser-agent benchmark.

## Pre-allocated STATUS row

Your row in `benchmark/tasks/STATUS.md` is **{{row}}**. After your task is built and tested, **YOU update this row** by editing the line that starts with `| {{row}} |` to fill in Status/Oracle/Browser-Use/F1, AND append a detailed section at the bottom of STATUS.md following the existing format. No other agent will touch this row, so you cannot collide.

## Worktree environment

You are in an isolated worktree pre-warmed from `.claude/worktree-skeleton`. The venv at `.venv/` already has all dependencies installed. The `.odoorc.local` is in place. **Do not run `uv pip install` or copy configs unless eval.py reports a specific missing dependency.**

## REQUIRED reading before writing code

1. `benchmark/ODOO19_PATTERNS.md` — known quirks. Saves rediscovery.
2. `benchmark/TASK_CREATION_GUIDE.md` — file-format reference.
3. The reference tasks listed below — copy patterns, don't reinvent.

Reference tasks for this build: {{reference_tasks}}

## Task spec

- **Workflow:** {{workflow}}
- **Hard pattern:** {{hard_pattern}}
- **Distinct from:** {{distinct_from}}
- **Check focus:** {{check_focus}}
- **Calibration risk:** {{calibration_risk}}

## Files to create

In `benchmark/tasks/{{task_id}}/`: task.yaml, prompt.md, seed.py, expected_state.json, state_spec.yaml, trace_spec.yaml, check.py, cleanup.py, oracle.py.

`task.yaml` must use: `tier: {{tier}}`, `time_limit_sec: {{time_limit_sec}}`, `step_limit: {{step_limit}}`.

## Lifecycle (OPTIMIZED)

1. Read the 3 required docs above.
2. Write all 9 files. Use Odoo 19 field names from the cookbook.
3. Run oracle: `PYTHONPATH=. .venv/bin/python benchmark/eval.py run {{task_id}} --agent human`. Iterate until PASSES (postconditions `[]`).
4. Run browser-use **ONCE**: `PYTHONPATH=. .venv/bin/python benchmark/eval.py run {{task_id}} --agent browser-use`.
   - If result is `PASS` or `FAIL` with non-zero steps and a postcondition trace, that's your data point. Move on.
   - If result is `ENV_CRASH` (ConnectionRefused, gave_up at step 0, no artifacts), retry ONCE more.
   - Do NOT run browser-use a second time just for confirmation. The first decisive result is the data point.
5. **Update STATUS.md row {{row}}** in place with the actual result. Format:
   ```
   | {{row}} | {{task_id}} [{{difficulty}}] | {{summary}} | Done | PASS | <PASS|FAIL|FAIL_strict_F1_{{f1}}> | {{f1}} |
   ```
   Then append a detailed section at the very end of STATUS.md (use existing detail-section format).
6. Update `benchmark/ODOO19_PATTERNS.md` — append any NEW quirks you discovered (not duplicating what's already there). Be terse.
7. Commit BOTH your task directory AND the STATUS.md / cookbook edits, in one commit:
   ```
   git add benchmark/tasks/{{task_id}}/ benchmark/tasks/STATUS.md benchmark/ODOO19_PATTERNS.md
   git commit -m "[ADD] benchmark: {{task_id}} task ({{difficulty}})"
   ```
8. **Do NOT push.** Parent will merge worktree branch.

## Calibration self-check

Before committing, ask: does the BU result match {{difficulty}} target?
- easy: ~80% pass — single PASS is fine
- medium: ~60% pass — single PASS or FAIL is informative; PASS is acceptable but flag in notes
- hard: ≤ 40% pass — single PASS suggests too easy; if so, add complexity (extra distractor, hidden field, non-default wizard option) and re-test once. If still PASS, commit anyway and flag in `calibration_note`.

## Report back (≤ 200 words)

- Oracle: PASS/FAIL
- Browser-use: PASS/FAIL/ENV_CRASH (1 or 2 attempts)
- F1 estimate
- Calibration: matches/easier/harder than tier
- New cookbook quirks added: yes/no, list
- Quirks/blockers
- Commit hash + branch name
```

### 2.3 — Pacing loop

Use `ScheduleWakeup` with `<<autonomous-loop-dynamic>>` to wake up periodically
(suggest 600–1200s based on average task wall time). On each wake:

1. Refresh `TaskList` to find newly completed agents.
2. For each completed agent:
   - Cherry-pick its commit into the current branch.
   - Move row from `in_flight` to `completed` in manifest.
   - Push to origin every 3–5 completions (or on stop).
3. Top up the pool: while `len(in_flight) < pool_size and pending_rows`:
   - Pop next pending row.
   - Launch a new Agent with the standardized prompt template.
   - Append to `in_flight`.
4. Check stop condition. If met, drain (wait for in-flight to finish) and go to Phase 3.

Use `TaskCreate` for each launched agent (and `TaskUpdate` on completion) so
the user can see live progress.

### 2.4 — Failure handling

- **Agent reports `aborted` (missing module):** mark the row as `Removed` in
  STATUS.md (manually, since the agent didn't), do not launch a replacement
  on that row, draw from backlog.
- **Agent's commit is empty / cherry-pick conflicts:** investigate; usually
  the agent failed before committing. Mark its row as `WIP` (leave for retry)
  and launch a different backlog entry instead.
- **Agent reports oracle FAIL after iteration:** the task is undoable as
  designed. Mark row `Removed` with reason; do not retry.
- **Multiple consecutive `ENV_CRASH`** across agents (≥ 3 in a row): pause the
  pool — the cleanup-collision patch from Phase 0.1 may have regressed. Tell
  the user before continuing.

---

## Phase 3 — Final consolidation and report

When stop condition is met:

1. Wait for all in-flight agents to finish (don't kill them mid-run).
2. Cherry-pick remaining commits.
3. Push final batch.
4. Print a summary table:
   - Total tasks completed
   - Wall-clock time
   - Mean F1
   - Pass-rate per difficulty tier (calibration health)
   - Removed tasks with reasons
   - New cookbook entries added
   - Average tokens per task (rough estimate from agent reports)

Persist the manifest to `.claude/relentless-pool/runs/<timestamp>.json` for
later inspection.

---

## State files this skill creates

```
.claude/worktree-skeleton/             # one-time, reused across runs
  .venv/
  .odoorc.local
.claude/relentless-pool/
  backlog.jsonl                        # generated each session
  manifest.json                        # current run state (live)
  runs/<ISO-timestamp>.json            # archived run summaries
```

```
benchmark/ODOO19_PATTERNS.md           # cookbook, grows over time
```

---

## When NOT to use this skill

- **First time on a new machine** — run a single sequential task first to
  shake out env issues. Then use this skill.
- **Task ideation is the goal, not throughput** — use
  `expand-benchmark-coverage` instead. This skill assumes the backlog is
  generated in bulk and built mechanically.
- **Calibration tightening pass** — this skill optimizes for *quantity*, not
  per-task tuning. If you need to revisit existing tasks (e.g., 5 mediums
  came in too easy), do that as a separate focused effort.

---

## Resuming a previous run

If interrupted mid-run, re-invoke `/relentless-benchmark-pool` with the same
arguments. The skill detects `manifest.json` and offers to resume. To start
fresh, delete `.claude/relentless-pool/manifest.json` first.
