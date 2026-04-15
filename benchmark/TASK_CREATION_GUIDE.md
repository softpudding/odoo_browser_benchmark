# Creating Difficult Benchmark Tasks for Browser Agents

## Overview

This guide documents the end-to-end workflow for creating benchmark tasks that
reliably fail browser-use (and similar browser agents) while remaining realistic
and completable by an instructed human. It was developed through iterative
empirical testing — designing tasks, running them against browser-use, analyzing
failures, and redesigning tasks that were too easy.

**Bottom line requirements for every task:**
1. **Realistic and doable** — an instructed human must be able to pass
2. **Clear instructions** — no ambiguity, no vague steps
3. **Not undoable** — the seed must create the exact state described in the prompt
4. **Adequate timeout** — complex tasks need 420–480s, not 300s

---

## Phase 1: Understand What Fails Browser Agents

### Proven failure patterns (empirically validated)

These patterns **consistently fail** browser-use:

| Pattern | Why it fails | Example |
|---------|-------------|---------|
| **Wizard with non-default radio buttons** | Agent clicks the default/first option instead of reading which to select | Backorder "Create Backorder" dialog, Calendar "This Event" vs "All Events" |
| **Create-from-scratch with exact fields** | Agent leaves phantom empty lines or misses fields | Creating a new PO with exact product lines |
| **Multi-step wizard with field entry** | Agent can't navigate complex modals with multiple fields to fill | Send by Email compose wizard, date pickers in wizards |
| **Cross-module round-trips** | Agent loses context when navigating away and back | Purchase → Inventory → back to Purchase |
| **Date picker manipulation** | Agent can't change dates in Odoo's date picker widget | Setting a specific credit note date in the reversal wizard |

### Patterns that do NOT fail browser-use (too easy)

These patterns are **consistently solved** by browser-use — avoid building tasks around them:

| Pattern | Why it's easy | Example |
|---------|-------------|---------|
| **Simple form edits** (change a field, save) | Direct field interaction, no wizard | Changing a quantity on a draft SO line |
| **Find-and-select** (open correct record from list) | Standard list navigation | Opening the right invoice among several |
| **Accept-defaults wizards** (open wizard, click OK) | No decision needed, just click through | "Create Invoice" wizard with Regular Invoice default, "Register Payment" with defaults |
| **Reset-to-draft → edit → re-post** | Linear 3-step sequence, no branching | Editing a posted invoice line |
| **Scrolling in long lists** | Browser-use handles viewport scrolling fine | Finding line 16 in a 20-line SO |

### Key insight

> The difficulty comes from **non-default choices in modal dialogs** and
> **creating records with exact field values**, NOT from long sequences of
> simple steps. A 10-step task of simple clicks is easier than a 3-step task
> with one wizard that requires a radio button selection.

---

## Phase 2: Design the Task

### Step 2.1: Choose a difficulty category

Pick one of these five categories (see `benchmark/tasks/CATEGORY_DESIGN.md`):

1. **Closed-loop cross-module** — leave a module, complete work elsewhere, return
2. **Policy trap (wizard)** — task requires navigating a complex wizard with non-default choices
3. **Side-effect trap (wizard)** — edit via wizard without corrupting adjacent data
4. **Recovery/rollback** — undo a mistake (cancel/reset) then redo correctly
5. **Deep UI interaction** — handle tricky UI widgets (recurrence dialogs, date pickers, popovers)

### Step 2.2: Identify the specific Odoo workflow

Choose a real Odoo workflow that involves at least ONE proven failure pattern.
Good sources:

- **Wizards to target**: Backorder confirmation, Send by Email (mail.compose),
  Credit Note reversal, Register Payment, Create Invoice, Recurrence update,
  Stock transfer validation, Activity scheduling
- **Create-from-scratch flows**: New PO, New SO, New invoice
- **Cross-module flows**: Sale → Invoice, Purchase → Receipt, SO → Project

### Step 2.3: Write the prompt FIRST

Before writing any code, write `prompt.md` as if you're instructing a human.
Rules:

- **Name every entity explicitly** — customer name, reference number, product names
- **State exact values** — quantities, prices, dates, text to enter
- **Describe the expected UI flow** — which buttons to click, in what order
- **Mention wizard interactions explicitly** — "In the dialog that appears, select X"
- **State what NOT to do** — rules section at the end
- **Match Odoo 19 button labels exactly** — e.g., "Confirm" not "Post" for invoices

### Step 2.4: Verify the workflow manually

Before writing seed.py, manually perform the workflow in Odoo to verify:

1. The buttons/menus exist with the labels you wrote
2. The wizard fields exist and are labeled as you described
3. The workflow produces the expected end state
4. There are no blocking errors or missing prerequisites

---

## Phase 3: Implement the Task

### File structure

Every task directory needs exactly these files:

```
benchmark/tasks/<module>.<task_name>/
├── task.yaml           # Task metadata
├── prompt.md           # Human-readable instruction
├── seed.py             # Database seeding script
├── expected_state.json # State diff oracle (atomic edits)
├── state_spec.yaml     # Which models/fields to track
├── trace_spec.yaml     # Required/forbidden API operations
├── check.py            # Postcondition validation script
└── cleanup.py          # Cleanup for re-runs
```

### 3.1: task.yaml

```yaml
task_id: module.task_name
module: module_name
difficulty: hard
instruction: see prompt.md
start_url: /odoo/module_name
login_context:
  login: admin
agent_interface: browser_only
db_seed:
  snapshot: benchmark_base
setup_script: seed.py
time_limit_sec: 480          # 420-480 for complex tasks
step_limit: 300              # 250-300 for complex tasks
metadata:
  category: one_of_five_categories
  failure_pattern: "One sentence describing what the agent will get wrong"
  primary_track: true        # true = included in primary benchmark results
  tier: 3                    # 3 = hardest tier
```

**Timeout guidelines:**
- Simple wizard task: 420s
- Cross-module or create-from-scratch: 480s
- Never use < 300s for hard tasks

### 3.2: seed.py

```python
"""One-line description of what this seeds.

Category N: category name.
Multi-line explanation of the difficulty design.
"""

def setup(env):
    # 1. Create/find required partners, products, etc.
    # 2. Cleanup prior runs (ALWAYS do this first)
    # 3. Create the exact state described in prompt.md
    # 4. Verify with env.cr.commit() if needed
```

**Critical seed.py rules:**

1. **Always clean up first** — search and delete records from prior runs
2. **Use the correct field names for Odoo 19:**
   - `tax_ids` not `tax_id` on `sale.order.line`
   - `group_ids` not `groups_id` on `res.users`
   - `memo` not `ref` on `account.payment`
   - `product_qty` not `quantity` on `purchase.order.line`
3. **Enable required features explicitly:**
   - Credit limit: `env["ir.config_parameter"].sudo().set_param("account.use_credit_limit", "True")`
   - SO line discounts: enable `sale.group_discount_per_so_line` group
   - These features may not be enabled in the base snapshot
4. **Clear taxes if your prompt quotes exact untaxed totals:**
   ```python
   "tax_ids": [(5, 0, 0)],  # Clear all taxes for clean math
   ```
5. **Set `invoice_policy`** on products if the task involves invoicing:
   ```python
   "invoice_policy": "order",  # or "delivery"
   ```
6. **Use `supplier_rank: 1`** for vendor partners in purchase tasks
7. **Cleanup must handle all states** — a record may be draft, posted, confirmed, cancelled from a prior failed run

### 3.3: expected_state.json

This file defines the **state diff** the eval engine checks. It only captures
**changes** from before to after — unchanged values do NOT appear here.

```json
[
  {
    "model": "sale.order",
    "entity_key": ["Customer Name", "REFERENCE"],
    "field": "state",
    "op": "set",
    "norm_value": "sale"
  }
]
```

**Critical rules for entity_key:**

The entity_key is built from the `match_key` fields in `state_spec.yaml`,
passed through `normalize_value()`:
- **Many2one** `[id, "Display Name"]` → `"Display Name"`
- **False/None** → `null`
- **Strings** → as-is
- **Datetimes** → tricky (XML-RPC format), avoid using as match keys

**Common pitfalls:**
- `order_id` on SO lines normalizes to `null` (not the SO name) — check via
  actual run output
- `move_id` on invoice lines normalizes to `null`
- For new records (create-from-scratch), use `"op": "create"` not `"set"`
- **Never use `"op": "eq"` or `"domain"` — the diff engine doesn't support them**
- Keep expected_state minimal — validate details via `check.py` instead
- When in doubt, run the task once and inspect `state_diff.json` to see the
  actual entity_keys and ops the engine produces

**Pro tip:** After your first run, check the `state_diff.json` output artifact
to see exactly what entity_keys the diff engine generates, then copy them into
your expected_state.json.

### 3.4: state_spec.yaml

```yaml
models:
  sale.order:
    match_key:
      - partner_id        # Many2one → normalizes to display name
      - client_order_ref  # Char → as-is
    fields:
      - partner_id
      - client_order_ref
      - state
    ignore_fields:
      - id
      - create_date
      - write_date
```

**Tips:**
- Don't track `account.move` by `ref` if the record is created during the task
  (ref may be null) — use `invoice_origin` or track only via check.py
- Don't use datetime fields as match_keys (XML-RPC serialization is fragile)
- Keep the model list small — only track what you assert in expected_state.json

### 3.5: check.py

This is your **most important validation file**. The diff engine only checks
state changes; check.py validates the full end state including unchanged values.

```python
def check(env):
    failures = []
    # ... validate everything ...
    return failures  # empty list = PASS
```

**What to validate in check.py:**
- Final record state (confirmed, posted, paid, etc.)
- Unchanged records weren't modified (distractor invoices still posted)
- Line-level details (quantities, prices, discounts)
- Specific field values that are hard to express as diffs (dates, text, memo)
- Record counts (no extra records created, no records deleted)

### 3.6: trace_spec.yaml

```yaml
required_ops:
  - sale.order.action_confirm    # Must have happened

optional_ops:
  - sale.order.read              # Fine if it happens
  - sale.order.web_save          # Browser often uses this instead of .write

forbidden_ops:
  - sale.order.unlink            # Must NOT happen
```

**Important:** The browser client often uses `web_save` instead of the ORM
`write` or `create` methods. If your required_ops list `model.create` but the
agent uses `web_save`, the required op will show as missed even though the
action succeeded. Put `create`/`write`/`web_save` in optional_ops and validate
the actual outcome via check.py instead.

### 3.7: cleanup.py

```python
def cleanup(env):
    # Reverse the seed — delete all records created by setup()
    # Must handle all possible states (draft, posted, cancelled)
```

---

## Phase 4: Run Against Browser-Use

### Step 4.1: Verify seed works

```bash
uv run benchmark-eval run <task_dir> --agent human
```

This runs the seed and lets you complete the task manually. Verify:
- Seed creates the described state (no warnings/errors)
- You can complete the task as described in prompt.md
- Postconditions pass after you complete it

### Step 4.2: Run against browser-use

```bash
uv run benchmark-eval run <task_dir> --agent browser-use
```

**Always use headed mode** (default) — never `--headless`. You need to observe
the agent's behavior to diagnose failures.

### Step 4.3: Interpret results

Check the output for three things:

1. **Seed success**: Look for `SEED_OK` in output. If you see `WARNING: seed
   may have failed`, check the stderr for the actual error (usually wrong field
   names).

2. **Agent behavior**: Watch the browser. Did the agent:
   - Find the right record?
   - Click the right buttons?
   - Handle the wizard correctly?
   - Get stuck somewhere specific?

3. **Scoring**: The output shows:
   ```
   RESULT: FAIL  (Strict: FAIL)
   StateDiffF1: ...
   Postcondition failures: ...
   ```
   - **FAIL + empty postconditions** = diff engine mismatch (fix expected_state.json)
   - **FAIL + postcondition failures** = genuine agent failure (task works!)
   - **PASS + empty postconditions** = agent solved it (task too easy, redesign)

### Step 4.4: Distinguish failure types

| Symptom | Cause | Action |
|---------|-------|--------|
| `seed may have failed` + `ValueError: Invalid field` | Wrong field name in seed.py | Fix the field name |
| `FAIL` but postconditions pass | entity_key mismatch in expected_state.json | Check `state_diff.json` artifact, copy real entity_keys |
| `FAIL` with genuine postcondition failures | Browser-use can't do this task | SUCCESS — task is hard enough |
| `PASS` with all postconditions passing | Browser-use solved the task | Task too easy — redesign with harder pattern |
| `ConnectionRefusedError` during post-task state capture | Odoo server died (DB dropped during run) | Infra collision — re-run |

---

## Phase 5: Iterate on Failed Designs

If browser-use passes your task, it's too easy. Apply these escalation strategies:

### Escalation ladder (in order of increasing difficulty)

1. **Add a wizard step** — Instead of direct form edit, require going through a
   wizard modal (e.g., "Register Payment" instead of editing payment_state)

2. **Require non-default wizard values** — Don't let the agent just click OK;
   require changing a date, filling a reason, selecting a non-default radio option

3. **Add create-from-scratch** — Require the agent to create a new record with
   exact field values (proven to leave phantom empty lines)

4. **Add cross-module navigation** — Require leaving one app and entering another
   mid-workflow

5. **Add radio/select dialog choices** — Calendar recurrence "This Event" vs
   "All Events", backorder "Create Backorder" vs "No Backorder"

6. **Combine multiple hard patterns** — e.g., create-from-scratch + send-by-email
   wizard (task 2 in our suite uses this)

### What was tried and failed (too easy)

- Simple "Reset to Draft → Edit → Re-post" on invoices
- "Find correct record among distractors → click Confirm"
- "Scroll to line 16 in a 20-line SO → edit it"
- "Open wizard → accept all defaults → click Create"
- "Register Payment → click Create Payment" (too few fields)
- "Create Invoice → click Create and View" (single-step wizard)
- "Full Credit Note → just reverse" (no non-default values needed)

### What actually works (hard enough)

- "Create Backorder" radio dialog in stock receipt validation
- "Send by Email" compose wizard (multiple fields: template, recipients, body)
- "Credit Note with specific date + partial qty edit" (date picker + line edit)
- "Cancel confirmed PO + create new PO with exact lines" (phantom line issue)
- "Edit single calendar occurrence" (recurrence update radio dialog)

---

## Phase 6: Cross-Review (Second Opinion)

### Limitation: never self-review

A model reviewing its own work has the same blind spots that produced the bugs
in the first place. The review **must** come from a different model:

| If you are...     | Ask for review from... | How |
|-------------------|------------------------|-----|
| **Claude Code**   | **Codex** (via `codex:rescue` agent) | Spawn a Codex agent with the review prompt below |
| **Codex**         | **Claude Code** | Hand the task files back to Claude Code and ask it to review |
| **A human**       | Either model, or another human | Use `--agent human` to test yourself, then ask a model to audit the files |

The point is: **always get a second opinion from a different reviewer**, not
from the same system that authored the task. Self-review consistently misses
field-name typos, entity-key format mismatches, and seed-prompt inconsistencies
because the author "knows what they meant" and reads past errors.

### Review prompt template

Whichever model you ask, use this prompt:

```
Review N benchmark tasks for browser agent evaluation.

User requirements:
1. Realistic and doable — an instructed human must be able to pass
2. Instructions must NOT be wrong or vague
3. Tasks must NOT be undoable
4. Complex instructions must NOT have only short timeouts

For each task, read ALL files and evaluate:
A. Instruction clarity
B. Doability in Odoo 19
C. Timeout adequacy
D. Seed-prompt consistency
E. Expected state correctness (entity_keys match diff engine)
F. check.py correctness
G. trace_spec correctness

Give a structured per-task verdict: PASS or ISSUE with specific actionable findings.
```

### What cross-review catches that self-review misses

From empirical experience building the first 5 tasks, every single task had
issues that the authoring model missed but the cross-reviewer caught:

- **Field names wrong** (Odoo 19 renames) — `tax_id` → `tax_ids`, `groups_id` → `group_ids`, `ref` → `memo`
- **Feature not enabled in seed** — credit limits, discount groups need explicit activation
- **Entity key format mismatch** — Many2one fields normalize differently than expected
- **Prompt button labels wrong** — "Post" vs "Confirm" on invoices
- **check.py logic bugs** — wrong count expectations after record creation/deletion
- **trace_spec too strict** — `create` in required_ops but agent uses `web_save`
- **Prompt references don't match seed** — prompt says "PO-PARTIAL-01" but seed uses "BENCH-PARTIAL"

These are exactly the kind of errors where a fresh pair of eyes (a different
model) catches what the author glosses over.

---

## Phase 7: Commit

Only commit tasks that satisfy ALL of:
- [ ] Seed runs without errors
- [ ] Human can complete the task (verified via `--agent human` or manual testing)
- [ ] Browser-use consistently fails (at least 2 runs)
- [ ] Failure is genuine (postcondition failures, not just diff mismatch)
- [ ] Codex review found no blocking issues
- [ ] expected_state.json entity_keys verified against actual `state_diff.json` output

---

## Appendix: Existing Hard Tasks (Do Not Duplicate)

The following 5 tasks already exist and reliably fail browser-use. New tasks
must target **different workflows, modules, or failure patterns** to avoid
overlap.

| # | Task ID | Module(s) | Wizard/UI involved | Failure pattern |
|---|---------|-----------|-------------------|-----------------|
| 1 | `purchase_stock.receive_and_complete_backorder` | purchase, stock | Backorder confirmation dialog (radio: Create Backorder / No Backorder) | Agent creates return instead of backorder; can't handle the radio dialog |
| 2 | `sale.create_quotation_and_send_email` | sale, mail | Send by Email compose wizard (template, recipients, subject, body) | Agent creates SO correctly but can't complete the email compose modal |
| 3 | `account.create_credit_note_and_reconcile` | account | Credit Note reversal wizard (reason, date, journal) + line qty edit | Agent creates credit note but fails to change the date in the wizard |
| 4 | `purchase.cancel_reissue_wrong_vendor` | purchase | N/A (create-from-scratch) | Agent leaves phantom empty line when creating new PO with exact lines |
| 5 | `calendar.edit_single_recurrence_occurrence` | calendar | Recurrence update dialog (radio: This Event / This and Following / All Events) | Agent selects "All Events" instead of "This Event" |

### Modules already covered
- `purchase` (2 tasks), `sale` (1), `account` (1), `calendar` (1), `stock` (1)

### Modules NOT yet covered (good candidates for new tasks)
- `crm` — lead conversion wizard, pipeline stage changes
- `hr_recruitment` — applicant processing, interview scheduling
- `project` — task creation with subtasks, timesheet entry
- `website` — page editing, form builder (DOM-heavy)
- `inventory` (standalone) — stock adjustments, scrap wizard
- `manufacturing` — work order processing, BOM management

### Failure patterns NOT yet exploited (good candidates)
- **Drag-and-drop** (Kanban stage changes, calendar event rescheduling)
- **Multi-record batch operations** (select multiple records → batch action wizard)
- **Inline tree editing** (editing cells directly in a list/tree view)
- **Chatter interactions** (posting notes, scheduling activities via popover)
- **Website/frontend editing** (Owl component manipulation, drag-drop blocks)
- **Import wizards** (CSV upload + field mapping dialog)
- **Nested wizard-within-wizard** (e.g., creating a new contact from within a SO form)

---

## Appendix: Field Name Reference (Odoo 19)

| Model | Common mistake | Correct field |
|-------|---------------|---------------|
| `sale.order.line` | `tax_id` | `tax_ids` |
| `res.users` | `groups_id` | `group_ids` |
| `account.payment` | `ref` (for memo) | `memo` |
| `purchase.order.line` | `quantity` | `product_qty` |
| `account.move.line` | `quantity` (display) | `quantity` (correct in v19) |
| `sale.order` | `validity_date` | `validity_date` (expiration) |

## Appendix: Running Tasks

All commands assume you are in the repo root and have [uv](https://docs.astral.sh/uv/) installed.
`uv run` automatically installs dependencies from `pyproject.toml` / `uv.lock`.

```bash
# Run single task against browser-use (always headed)
uv run benchmark-eval run <task_dir> --agent browser-use

# Run as human tester
uv run benchmark-eval run <task_dir> --agent human

# List all tasks
uv run benchmark-eval list

# Clean up orphan processes after a crash
uv run benchmark-eval cleanup

# Re-score a completed run
uv run benchmark-eval score <output_dir> --task <task_dir>

# Install new modules in benchmark DB + rebuild snapshot
.venv/bin/python3 odoo-bin -d benchmark_validate -i module1,module2 -c .odoorc.local --stop-after-init
uv run benchmark-eval prepare-base --db benchmark_validate
```
