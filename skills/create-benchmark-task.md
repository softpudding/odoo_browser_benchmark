---
name: create-benchmark-task
description: Create a new hard benchmark task for browser agent evaluation. Generates all required files (prompt.md, seed.py, task.yaml, expected_state.json, check.py, trace_spec.yaml, state_spec.yaml, cleanup.py), validates against known difficulty patterns, and runs against browser-use. Use when adding new tasks to the benchmark suite.
user-invocable: true
argument-hint: [module.task_name]
---

# Create a Hard Benchmark Task

You are creating a new benchmark task named `$ARGUMENTS` for evaluating browser
agents on Odoo ERP workflows. The task MUST reliably fail browser-use while
being completable by an instructed human.

**Read the full guide first:** `benchmark/TASK_CREATION_GUIDE.md`

---

## Step 1: Validate the task name

The argument `$ARGUMENTS` should follow the pattern `module.descriptive_name`
(e.g., `crm.convert_lead_to_opportunity`). If no argument was given, ask the
user what workflow they want to target.

Check that the task doesn't already exist:
```
ls benchmark/tasks/$ARGUMENTS/ 2>/dev/null
```

Check existing tasks to avoid duplication:
```
PYTHONPATH=. python benchmark/eval.py list
```

---

## Step 2: Choose a difficulty pattern

The task MUST use at least one of these **proven failure patterns** — tasks
built around other patterns will likely be too easy:

1. **Wizard with non-default radio buttons** — Agent must select a specific
   non-default option in a dialog (e.g., "This Event" in recurrence, "Create
   Backorder" in stock receipt)

2. **Create-from-scratch with exact fields** — Agent must create a new record
   and fill exact product lines, quantities, prices (browser-use leaves phantom
   empty lines)

3. **Multi-step wizard with field entry** — Agent must fill multiple fields in
   a wizard modal (date pickers, text fields, not just click OK)

4. **Cross-module round-trip** — Agent must navigate away to another module
   and come back (loses context)

5. **Complex compose/email wizard** — The "Send by Email" compose wizard has
   template, recipients, subject, body fields

**DO NOT use these patterns alone** (browser-use solves them easily):
- Simple form edits (change field, save)
- Accept-defaults wizards (open wizard, click OK)
- Reset-to-draft → edit → re-post cycles
- Scrolling in long lists
- Find-correct-record-and-click-confirm

---

## Step 3: Design the prompt

Write `prompt.md` FIRST, before any code. Rules:
- Name every entity explicitly (customer name, reference, product names)
- State exact values (quantities, prices, dates)
- Describe expected UI flow with button labels matching Odoo 19
- Mention wizard interactions explicitly
- Add a **Rules** section listing what NOT to do
- **Verify button labels** — Odoo 19 uses "Confirm" not "Post" for invoices

---

## Step 4: Create all 8 files

Create the directory and all files:

```
benchmark/tasks/$ARGUMENTS/
├── task.yaml
├── prompt.md
├── seed.py
├── expected_state.json
├── state_spec.yaml
├── trace_spec.yaml
├── check.py
└── cleanup.py
```

### task.yaml template
```yaml
task_id: $ARGUMENTS
module: <module_name>
difficulty: hard
instruction: see prompt.md
start_url: /odoo/<module_name>
login_context:
  login: admin
agent_interface: browser_only
db_seed:
  snapshot: benchmark_base
setup_script: seed.py
time_limit_sec: 480        # 420-480 for hard tasks, NEVER < 300
step_limit: 300
metadata:
  category: <one of: closed_loop_cross_module, policy_trap, side_effect_trap, recovery_rollback, deep_ui_interaction>
  failure_pattern: "One sentence: what browser-use will get wrong"
  primary_track: true
  tier: 3
```

### seed.py critical rules
- **Always cleanup prior runs first**
- Use correct Odoo 19 field names: `tax_ids` (not `tax_id`), `group_ids` (not `groups_id`), `memo` (not `ref` on payment), `product_qty` (not `quantity` on PO line)
- Enable required features: credit limits via `ir.config_parameter`, discount groups via `sale.group_discount_per_so_line`
- Clear taxes with `"tax_ids": [(5, 0, 0)]` if prompt quotes exact untaxed totals
- Set `invoice_policy: "order"` on products for invoicing tasks
- Use `supplier_rank: 1` for vendor partners

### expected_state.json rules
- Only include **actual state changes** (not unchanged values)
- Entity keys come from state_spec match_key fields, normalized: Many2one → display name, False → null
- Use `"op": "set"` for changes, `"op": "create"` for new records
- **Never use `"op": "eq"`, `"domain"`, or `"__count__"`** — unsupported
- Keep it minimal — validate details in check.py instead
- **Pro tip**: Run once, check `state_diff.json` artifact for real entity keys

### check.py rules
This is the most important validation file. Validate:
- Final record state (confirmed, posted, paid, etc.)
- Unchanged/distractor records weren't modified
- Line-level details (quantities, prices, discounts, dates)
- Record counts (no extra records, no deletions)
- Specific field values (memo text, dates, reasons)

### trace_spec.yaml rules
- Put wizard action methods in `required_ops` (e.g., `refund_moves`, `action_create_payments`)
- Put `create`/`write`/`web_save` in `optional_ops` (browser uses `web_save` instead of ORM methods)
- Put destructive operations in `forbidden_ops` (`unlink`, `button_cancel`, etc.)

---

## Step 5: Check if required modules are installed

Verify the module is in the base snapshot:
```bash
psql -tAc "SELECT name FROM ir_module_module WHERE state='installed' AND name='<module>'" benchmark_validate
```

If not installed:
```bash
.venv/bin/python3 odoo-bin -d benchmark_validate -i <module> -c .odoorc.local --stop-after-init
PYTHONPATH=. python benchmark/eval.py prepare-base --db benchmark_validate
```

---

## Step 6: Test as human first

```bash
PYTHONPATH=. python benchmark/eval.py run $ARGUMENTS --agent human
```

Verify:
- Seed runs without errors (no `WARNING: seed may have failed`)
- You can complete the task following prompt.md exactly
- Postconditions pass (empty `[]`)

---

## Step 7: Run against browser-use

```bash
PYTHONPATH=. python benchmark/eval.py run $ARGUMENTS --agent browser-use
```

**Always headed mode** (default). Never `--headless`.

Interpret the result:
- `FAIL + postcondition failures` → Task works! Genuine agent failure.
- `FAIL + empty postconditions` → Diff engine mismatch. Check `state_diff.json`, fix entity keys.
- `PASS` → Task too easy. Go back to Step 2, add a harder pattern.
- `seed may have failed` → Fix field names in seed.py.

If it FAILS, run a second time to verify consistency.

---

## Step 8: Cross-review (MANDATORY — never self-review)

**You must get a second opinion from a DIFFERENT model.** Self-review misses
the same blind spots that produced the bugs. Every task in the original suite
had issues caught only by cross-review.

- **If you are Claude Code**: delegate the review to Codex via `codex:rescue` agent
- **If you are Codex**: hand the files back to Claude Code for review

The reviewer should check: A. Instruction clarity, B. Doability, C. Timeout
adequacy, D. Seed-prompt consistency, E. Expected state correctness, F. check.py
correctness, G. trace_spec correctness.

Fix any blocking issues the reviewer finds, then re-run against browser-use.

---

## Step 9: Commit

Only commit if ALL of these are true:
- [ ] Seed runs without errors
- [ ] Human can complete the task
- [ ] Browser-use fails consistently (2+ runs)
- [ ] Failure is genuine (postcondition failures, not just diff mismatch)
- [ ] Codex review passed (no blocking issues)
- [ ] Task doesn't duplicate an existing task's workflow
