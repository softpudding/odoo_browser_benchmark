---
name: validate-benchmark-tasks
description: Randomly select 10% of benchmark tasks and validate them by running human mode (via tmux) and browser-use in parallel. Compares results, diagnoses task design failures, and produces a validation report for the paper.
user-invocable: true
argument-hint: "[--all | --tasks task1,task2 | --pct 10]"
---

# Validate Benchmark Tasks (Human vs Agent)

You are running a human-validation workflow for the Odoo browser agent benchmark.
The goal: prove each task is actually completable by a human (not a task design
failure) and collect human vs browser-use comparison data for the paper in `paper/`.

## Overview

For each selected task:
1. Launch **human mode** in a tmux pane (interactive — the user performs the task)
2. Launch **browser-use** in a parallel tmux pane (automated agent)
3. After both finish, compare scores and diagnose any failures

---

## Step 1: Select tasks

Parse `$ARGUMENTS` to determine which tasks to validate:

- `--all` — validate every task
- `--tasks task1,task2,...` — validate specific tasks by name
- `--pct N` — randomly select N% of all tasks (default: 10%)
- No arguments — default to 10% random selection

List all available tasks:
```bash
uv run benchmark-eval list
```

To randomly select 10% of tasks, use Python:
```bash
python3 -c "
import random, yaml
from pathlib import Path
tasks_dir = Path('benchmark/tasks')
all_tasks = sorted(d.name for d in tasks_dir.iterdir() if (d / 'task.yaml').exists())
n = max(1, len(all_tasks) * 10 // 100)
selected = random.sample(all_tasks, n)
print('\n'.join(selected))
"
```

Tell the user which tasks were selected and ask for confirmation before proceeding.

---

## Step 2: Ensure tmux is available

Check that tmux is running or start a session:
```bash
tmux has-session -t benchmark 2>/dev/null || tmux new-session -d -s benchmark
```

The workflow uses a tmux session named `benchmark` with two panes:
- **Left pane**: human eval (interactive — user reads instructions and performs task)
- **Right pane**: browser-use eval (automated — runs in background)

---

## Step 3: For each task, run human + browser-use in parallel

For each selected task, do the following:

### 3a. Create output directories

```bash
TASK_NAME="<task_name>"
TIMESTAMP=$(date +%s)
HUMAN_OUT="benchmark/reports/human_eval/${TASK_NAME}__human__${TIMESTAMP}"
AGENT_OUT="benchmark/reports/runs/${TASK_NAME}__browser-use__${TIMESTAMP}"
mkdir -p "$HUMAN_OUT" "$AGENT_OUT"
```

### 3b. Set up tmux layout

```bash
# Kill old panes, set up fresh split
tmux kill-session -t benchmark 2>/dev/null
tmux new-session -d -s benchmark -x 200 -y 50

# Left pane: human eval (this is the interactive pane)
tmux send-keys -t benchmark "uv run benchmark-eval run ${TASK_NAME} --agent human --no-isolate --output-dir ${HUMAN_OUT}" Enter

# Right pane: browser-use eval (automated)
tmux split-window -h -t benchmark
tmux send-keys -t benchmark "uv run benchmark-eval run ${TASK_NAME} --agent browser-use --provider dashscope --output-dir ${AGENT_OUT}" Enter
```

IMPORTANT: The human pane is interactive. Tell the user:

```
Task: {TASK_NAME}

I've set up tmux with two panes:
  - LEFT pane: Your human eval (interactive — follow the instructions shown)
  - RIGHT pane: browser-use agent (running automatically)

To attach to the tmux session:
  ! tmux attach -t benchmark

The LEFT pane will show you the exact same instructions the agent sees.
Read them carefully and complete the task in Odoo.
Press ENTER in the left pane when done.

When you're finished, detach from tmux (Ctrl+B then D) and come back here.
```

### 3c. Wait for both to complete

After the user reports they are done, check that both runs produced output:

```bash
# Check human result
cat "${HUMAN_OUT}/score.json" 2>/dev/null || echo "Human run not yet complete"

# Check agent result
cat "${AGENT_OUT}/score.json" 2>/dev/null || echo "Agent run not yet complete"
```

---

## Step 4: Compare results

For each completed task, read both score files and compare:

```bash
echo "=== ${TASK_NAME} ==="
echo "--- Human ---"
cat "${HUMAN_OUT}/score.json"
echo "--- Browser-use ---"
cat "${AGENT_OUT}/score.json"
```

Build a comparison table:

| Metric | Human | Browser-use |
|---|---|---|
| outcome_success | | |
| strict_success | | |
| state_diff_f1 | | |
| wall_clock_sec | | |
| missing_edits | | |
| extra_edits | | |

---

## Step 5: Diagnose failures

### If human PASSED but agent FAILED:
This is the expected case for hard tasks. Note it as "task validated".

### If human FAILED:
This is a potential task design problem. Investigate:

1. Read the task's `prompt.md` — is the instruction ambiguous?
2. Read `expected_state.json` — is the expected state achievable?
3. Read `state_diff.json` from the human run — what did the human actually do?
4. Compare human's observed diff vs expected diff — where do they diverge?

Common task design problems:
- **Ambiguous instruction**: the prompt allows multiple valid interpretations
- **Wrong expected state**: the oracle doesn't match what a correct execution produces
- **Missing seed data**: seed.py doesn't set up the right preconditions
- **Flaky state_spec**: fields that change due to side effects (timestamps, sequences)

If you find a task design problem, fix it immediately:
- Edit the relevant file (prompt.md, expected_state.json, seed.py, etc.)
- Re-run the human eval to verify the fix
- Note the fix in the validation report

If the human simply made a mistake, explain what went wrong and offer to re-run.

### If both FAILED:
Likely a task design or infrastructure problem. Check:
- Is the Odoo server running and healthy?
- Does the seed script work? (`uv run benchmark-eval run <task> --keep-db` then inspect)
- Is the snapshot valid?

---

## Step 6: Produce validation report

After all tasks are validated, write a summary report:

```bash
REPORT="benchmark/reports/human_eval/validation_report_$(date +%Y%m%d_%H%M%S).md"
```

The report should contain:

```markdown
# Human Validation Report

Date: <today>
Tasks validated: N / Total
Selection method: random 10%

## Results

| Task | Human | Agent | Status | Notes |
|---|---|---|---|---|
| task_name | PASS/FAIL | PASS/FAIL | validated/design-fix/rerun | ... |

## Task Design Fixes Applied
- task_name: description of fix

## Summary
- X/N tasks validated (human passed)
- Y/N tasks passed by agent
- Z task design issues found and fixed
```

Save this report and tell the user where to find it. This data feeds into
the paper at `paper/browser_agent_eval`.
