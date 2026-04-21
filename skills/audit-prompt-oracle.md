---
name: audit-prompt-oracle
description: Walk through benchmark tasks to find fundamental prompt-vs-oracle discrepancies — cases where the prompt is factually wrong and would block a competent human. NOT for style, detail level, or minor phrasing differences.
user-invocable: true
argument-hint: "[task_name | --all | --continue | --claim N]"
---

# Audit Prompt vs Oracle — Find Obvious Discrepancies Only

You are auditing benchmark tasks to catch **fundamental errors** in `prompt.md`
by cross-referencing against `oracle.py`.

## Philosophy — Read This First

This is a **benchmark project** testing browser agents. Prompts are deliberately
written at a natural level — they tell you *what* to accomplish, not *how* to
click through every screen. That is by design. A good prompt might say "create a
vendor bill from the purchase order" without specifying the exact button label or
navigation path. That's fine — figuring out the UI is part of the test.

**You are NOT here to:**
- Turn prompts into step-by-step SOPs mirroring the oracle
- Flag differences in detail level (prompt is vague, oracle is specific)
- Flag that oracle uses a helper function the prompt doesn't mention
- Flag differences in navigation style (prompt says "go to app X" vs oracle
  navigates to a specific URL)
- Flag field label vs technical field name differences
- Add more instructions to make the task easier

**You ARE here to find cases where the prompt is factually wrong or
incomplete in a way that causes failure:**
- Prompt names a button/action that **does not exist** in the UI
  (e.g., "click Create Bill" when the button is actually "Upload Bill" and does
  something completely different)
- Prompt describes a workflow that is **impossible** in the current Odoo version
  (e.g., "use the form-level button" when the action only exists as a list-view
  bulk operation)
- Prompt references a menu item or view that **doesn't exist**
- Prompt instructs a step order that would **cause an error** (e.g., "confirm
  before saving" when unsaved changes would be lost)
- Prompt **omits a critical step** that the oracle performs and check.py
  validates (e.g., prompt says fix qty/discount but oracle also fixes prices
  from negative to positive, and check requires positive total)
- Prompt specifies **wrong data values** (wrong amount, wrong label for a
  priority level, wrong date) compared to what oracle fills and check validates
- **check.py has a bug** that would fail correct UI work (e.g., timezone
  comparison inconsistency vs. other tasks in the same module)
- Two tasks are **exact duplicates** (same prompt, oracle, check, target
  record name) — they'd conflict on the same DB snapshot

The bar is high: **would a competent Odoo user get stuck, do the wrong thing,
or fail the automated check because the prompt is factually incorrect or
incomplete?** If yes, flag it. If they'd just need to explore the UI a bit,
that's fine — it's a benchmark.

---

## Coordination — Multiple Workers

This skill supports multiple workers auditing in parallel. Coordination uses a
single shared file:

```
benchmark/reports/prompt_oracle_audit.jsonl
```

Each line is a JSON object representing one task's status:

```jsonl
{"task": "account.create_bill_from_confirmed_po", "status": "claimed", "worker": "alice", "ts": "2026-04-21T14:00:00"}
{"task": "calendar.create_single_event", "status": "done", "worker": "bob", "ts": "2026-04-21T14:05:00", "verdict": "OK"}
{"task": "crm.update_lead_email", "status": "done", "worker": "bob", "ts": "2026-04-21T14:10:00", "verdict": "DISCREPANCY", "issue": "prompt says click Create Lead but button is New"}
```

### Statuses

- `claimed` — worker has reserved this task; others should skip it
- `done` — worker finished auditing; verdict is recorded

### Workflow

#### Step 0: Identify the worker

Determine the worker name. Use the git user name:

```bash
git config user.name
```

Use the first name (lowercased) as the worker ID. E.g., "Xiao Yang" → "xiao".

#### Step 1: Claim tasks

Before starting work, the worker **claims** a batch of tasks by appending
`claimed` lines to the JSONL file, then committing and pushing.

Parse `$ARGUMENTS` for batch size:
- `--claim N` — claim N unclaimed tasks (default: 10)
- A single task name — claim and audit just that one
- `--all` — claim all unclaimed tasks (solo mode)

To find unclaimed tasks:

```python
import json
from pathlib import Path
from datetime import datetime

audit_file = Path("benchmark/reports/prompt_oracle_audit.jsonl")
tasks_dir = Path("benchmark/tasks")

# All auditable tasks
all_tasks = sorted(
    d.name for d in tasks_dir.iterdir()
    if (d / "prompt.md").exists() and (d / "oracle.py").exists()
)

# Already claimed or done
taken = set()
if audit_file.exists():
    for line in audit_file.read_text().strip().splitlines():
        entry = json.loads(line)
        taken.add(entry["task"])

unclaimed = [t for t in all_tasks if t not in taken]
```

Claim by appending lines and committing:

```python
with open(audit_file, "a") as f:
    for task in batch:
        entry = {"task": task, "status": "claimed", "worker": worker, "ts": now}
        f.write(json.dumps(entry) + "\n")
```

Then **git add, commit, and push** the file so other workers see the claims:

```bash
git add benchmark/reports/prompt_oracle_audit.jsonl
git commit -m "audit: ${worker} claims ${N} tasks"
git push
```

Tell the user which tasks were claimed and how many remain unclaimed.

#### Step 2: Pull before starting

Before auditing, pull to pick up any new claims or results from others:

```bash
git pull --rebase
```

Re-read the JSONL to confirm your claims are still valid (conflict resolution:
if another worker claimed the same task, skip it).

#### Step 3: Audit claimed tasks

Work through your claimed tasks one by one (see "Auditing" section below).

After finishing each task, **append** a `done` line to the JSONL:

```python
entry = {"task": task, "status": "done", "worker": worker, "ts": now, "verdict": "OK"}
# or for discrepancies:
entry = {"task": task, "status": "done", "worker": worker, "ts": now, "verdict": "DISCREPANCY", "issue": "..."}
```

Commit and push periodically (every 5-10 tasks, or after fixing a discrepancy)
so colleagues see progress:

```bash
git add benchmark/reports/prompt_oracle_audit.jsonl
# also add any fixed prompt.md files
git commit -m "audit: ${worker} finished N tasks (M discrepancies)"
git push
```

#### Step 4: Check overall progress

To see how the audit is going:

```python
from collections import Counter
status = Counter()
workers = Counter()
for line in open(audit_file):
    entry = json.loads(line)
    if entry["status"] == "done":
        status[entry["verdict"]] += 1
        workers[entry["worker"]] += 1
    else:
        status["claimed"] += 1

total = len(all_tasks)
done = status["OK"] + status.get("DISCREPANCY", 0)
print(f"Progress: {done}/{total} done, {status['claimed']} claimed, {total-done-status['claimed']} unclaimed")
print(f"Verdicts: {dict(status)}")
print(f"Workers: {dict(workers)}")
```

---

## Auditing — Per-Task Process

For each claimed task, read all three files:

```
Read: benchmark/tasks/{task_name}/prompt.md
Read: benchmark/tasks/{task_name}/oracle.py
Read: benchmark/tasks/{task_name}/check.py
```

Reading check.py is essential — it tells you what actually gets validated. If
the oracle fixes a field that the prompt never mentions, check.py tells you
whether that matters (if check.py validates it, the omission is a real problem).
Also watch for check.py bugs like missing timezone conversion or wrong expected
values.

### What to check

Only flag **obvious discrepancies** — things that are factually wrong:

1. **Non-existent UI element**: Prompt names a specific button, menu item, or
   link that does not exist. The oracle clicks something with a fundamentally
   different name or location.

2. **Impossible workflow**: Prompt describes a path through the UI that cannot
   work. Example: prompt says to do X from the form view, but X is only
   available as a list-view bulk action.

3. **Wrong target/destination**: Prompt says to navigate somewhere that leads to
   the wrong view entirely.

4. **Data value mismatches**: Compare EVERY concrete value (amounts, dates,
   names, emails, references) between prompt and oracle. If prompt says "500"
   but oracle fills "5000", that's a discrepancy. Also check for **missing
   critical data steps** — if the oracle fixes a field (e.g., flipping negative
   prices to positive) that the prompt never mentions, and check.py validates
   that field, then the prompt is incomplete and an agent following it would
   fail.

5. **check.py bugs**: Read check.py too (not just prompt + oracle). If check.py
   validates something differently from how a UI agent would produce it (e.g.,
   comparing raw UTC times without timezone conversion when other similar checks
   do convert), flag it. A check.py bug means correct UI work gets marked wrong.

6. **Duplicate / conflicting tasks**: If two task directories have identical or
   near-identical prompt.md, oracle.py, and check.py (same contact name, same
   values), flag both. They would conflict if run on the same database snapshot.

7. **Task name vs content mismatch**: If the directory name implies one thing
   (e.g., "update_contact_mobile") but the prompt/oracle/check all operate on a
   completely different field (e.g., website), flag it. This indicates a
   copy-paste error during task creation.

### What NOT to flag

- Prompt says "set the reference" and oracle fills field `ref` → OK
- Prompt doesn't mention clearing search filters but oracle does → OK
- Prompt says "click Confirm" and oracle uses `click_status_button("Confirm")` → OK
- Prompt describes fewer steps than oracle performs → OK
- Prompt uses different wording for the same concept → OK

### Classify

- **OK** — no factual errors; prompt may be vague but not wrong
- **DISCREPANCY** — prompt contains a factual error that would block or mislead
  a competent user → **fix needed**

### Report each task

```
## {task_name}: OK
```

or

```
## {task_name}: DISCREPANCY
Problem: <what's factually wrong>
Prompt says: <the incorrect instruction>
Oracle does: <what actually works>
```

### Fix DISCREPANCY prompts

When fixing:

1. Make the **minimum change** to remove the factual error
2. Do NOT add detail, extra steps, or make the prompt more hand-holdy
3. Keep the same tone and abstraction level
4. The fix should make the prompt *not wrong*, not make it *more helpful*

Example of a good fix:
- Before: "Click the **Create Bill** button (in the status bar at the top)"
- After: "Create a vendor bill from this purchase order"
- NOT: "Select the PO checkbox in list view, then click Create Bills in the
  header toolbar that appears"

The last version is too detailed — it turns a benchmark prompt into an SOP.

---

## Summary Report

After all tasks across all workers are done, any worker can generate the report:

```
benchmark/reports/prompt_oracle_audit_report_YYYYMMDD.md
```

```markdown
# Prompt vs Oracle Audit Report

Date: <today>
Tasks audited: N (by K workers)
Workers: alice (X tasks), bob (Y tasks)

## Summary

- OK: X tasks
- DISCREPANCY: Y tasks (fixed)

## Discrepancies Found and Fixed

| Task | Problem | Fix Applied | Worker |
|---|---|---|---|
| task_name | button doesn't exist in UI | removed specific button name | alice |
```

Only list the discrepancies. Don't enumerate hundreds of OK tasks.
