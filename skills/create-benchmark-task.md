---
name: create-benchmark-task
description: Create a new benchmark task (hard, medium, or easy) for browser agent evaluation. Generates all required files (prompt.md, seed.py, task.yaml, expected_state.json, check.py, trace_spec.yaml, state_spec.yaml, cleanup.py), validates against difficulty patterns, and runs against browser-use. Use when adding new tasks to the benchmark suite.
user-invocable: true
argument-hint: [module.task_name] [hard|medium|easy]
---

# Create a Benchmark Task

You are creating a new benchmark task named `$ARGUMENTS` for evaluating browser
agents on Odoo ERP workflows.

## WORKTREE REQUIREMENT

**You MUST work in a separate git worktree for this skill.** The workflow is:

1. **Main branch first** — Steps 0–1 (validation, duplicate check) and Step 1b
   (reserve task name in STATUS.md, commit, push) happen on the main branch.
2. **Enter worktree** — After reserving the name, use `EnterWorktree`. All real
   work (file creation, seed writing, testing, iteration) happens in the worktree.
3. **Exit worktree** — Only exit (which merges changes back) once the task is
   complete or you are done.

**Read the full guide first:** `benchmark/TASK_CREATION_GUIDE.md`

---

## Step 0: Determine the target difficulty

The argument `$ARGUMENTS` may include a difficulty hint (e.g.
`sale.confirm_order easy`). If no difficulty was specified, ask the user before
proceeding. The three levels are:

| Level  | Target browser-use pass rate | Tier | Time limit   |
|--------|------------------------------|------|--------------|
| hard   | ≤ 40 %                       | 3    | 420 – 480 s  |
| medium | ~ 60 %                       | 2    | 300 – 360 s  |
| easy   | ~ 80 %                       | 1    | 180 – 240 s  |

**Difficulty asymmetry: too hard is acceptable, too easy is not.** If a task
turns out harder than its intended tier (e.g., an easy task that browser-use
fails), that is acceptable — the benchmark still measures real capability.
A task that ends up easier than intended is NOT acceptable, because it inflates
agent scores. When in doubt, keep requirements strict rather than relaxing them.

The sections below describe each level in detail so you can pick the right
interaction pattern and write the right checks.

---

## Difficulty reference

### Hard (tier 3) — browser-use should fail 60 %+ of runs

**How the agent must interact with Odoo:**
- Navigates across two or more modules (e.g. Sales → Contacts → back)
- Encounters at least one dialog or wizard where the correct option is *not*
  the default
- Must carry a value read in one place and apply it somewhere else (memory)
- Distractors: two or more records look similar; wrong record choice silently
  passes surface checks

**What the checks actually verify:**
- Exact line-item fields (product, quantity, price, discount) on the final record
- That distractor records were *not* modified
- The specific wizard option that was chosen (e.g., "This Event" vs "All
  Events", "Create Backorder" vs "No Backorder")
- Multi-record state after a cancel-and-reissue or rollback workflow

**Proven hard patterns (use at least one):**
1. Wizard with non-default radio button — agent must select a specific option
2. Create-from-scratch with exact fields — browser-use leaves phantom empty lines
3. Multi-field wizard — date pickers, text fields, not just click OK
4. Cross-module round-trip — agent navigates away, loses context, must return
5. Complex compose/email wizard — template, recipients, subject, body fields

---

### Medium (tier 2) — browser-use should pass ~60 % of runs

**How the agent must interact with Odoo:**
- Stays in one or two related modules without a full context switch
- May encounter a single wizard, but the default option is usually correct
- Needs to find the right record (one level of filtering), then make a targeted
  edit or trigger a workflow step
- At most one piece of information must be carried from one screen to another

**What the checks actually verify:**
- Primary record reaches the expected state (confirmed, posted, done, etc.)
- One or two key field values (memo text, a date, a partner name)
- No extra or missing records (count check)
- A single workflow action completed (email sent, payment registered, etc.)

**Suitable medium patterns:**
- Single-step wizard with at most one non-default field
- Form edit requiring navigation to the right record but no cross-module hop
- Sequential action on one record: open → edit → trigger button → verify
- Lookup-and-apply where both the lookup and the apply are in the same module

---

### Easy (tier 1) — browser-use should pass ~80 % of runs

**How the agent must interact with Odoo:**
- Direct navigation to a single, clearly identified record
- Basic form editing: fill a field, flip a toggle, or click a single button
- Accept-defaults dialogs where clicking OK or Confirm is sufficient
- No distractors; the record can be found by a unique name or reference

**What the checks actually verify:**
- A single field value changed on one record
- Workflow state after a single button click (e.g., draft → confirmed)
- Optional: a simple linked record created (e.g., a chatter message posted)

**Suitable easy patterns:**
- Simple field edit + save (change a date, a partner, a quantity)
- Accept-defaults wizard (open dialog, click OK, verify result)
- Reset to draft → change one field → re-confirm
- Add a note / log a message in the chatter

**Note:** If the task concept is interesting but trivially easy, consider
combining two easy steps (e.g., edit a field *and* confirm) to push it to
medium rather than discarding it.

---

## Step 1: Validate the task name and check for duplicates

The argument should follow the pattern `module.descriptive_name`
(e.g., `crm.convert_lead_to_opportunity`). If no argument was given, ask the
user what workflow they want to target.

Check the task doesn't already exist:
```
ls benchmark/tasks/<task_name>/ 2>/dev/null
```

**Read STATUS.md to check for conceptual duplicates:**
```
cat benchmark/tasks/STATUS.md
```

For each existing task, compare along three dimensions:
1. **Odoo modules** — same module(s)?
2. **Workflow type** — same kind of action (cancel+reissue, cross-module lookup,
   wizard interaction, etc.)?
3. **Capability tested** — same failure/success pattern?

**A new task must be distinct in at least two of the three dimensions.**

If the task is a duplicate, stop and tell the user which existing task covers
the same ground.

---

## Step 1b: Reserve the task name (on main branch, before worktree)

Add a WIP row to `benchmark/tasks/STATUS.md` to claim the task name and prevent
teammates from creating a duplicate while you work:

```markdown
| N | <task_name> [<difficulty>] | <one-line description> | WIP | — | — | — |
```

Commit and push immediately:

```bash
git add benchmark/tasks/STATUS.md
git commit -m "[WIP] benchmark: reserve <task_name> task"
git push upstream odoo_benchmark
```

**Now enter the worktree** with `EnterWorktree`. All remaining steps happen
inside the worktree.

---

## Step 2: Design the prompt

Write `prompt.md` FIRST, before any code. Rules:
- Name every entity explicitly (customer name, reference, product names)
- State exact values (quantities, prices, dates)
- Describe expected UI flow with button labels matching Odoo 19
- Mention wizard interactions explicitly
- Add a **Rules** section listing what NOT to do
- **Verify button labels** — Odoo 19 uses "Confirm" not "Post" for invoices
- Adjust prompt complexity to match the chosen difficulty: hard prompts may
  describe a multi-step workflow; easy prompts describe one clear action

---

## Step 3: Create all 8 files

```
benchmark/tasks/<task_name>/
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
task_id: <module.task_name>
module: <module_name>
difficulty: <hard|medium|easy>
instruction: see prompt.md
start_url: /odoo/<module_name>
login_context:
  login: admin
agent_interface: browser_only
db_seed:
  snapshot: benchmark_base
setup_script: seed.py
time_limit_sec: <420-480 hard | 300-360 medium | 180-240 easy>
step_limit: <300 hard | 200 medium | 120 easy>
metadata:
  category: <closed_loop_cross_module | policy_trap | side_effect_trap | recovery_rollback | deep_ui_interaction>
  difficulty_level: <hard|medium|easy>
  agent_interaction: "<one sentence: how the agent must navigate/interact>"
  checks_verify: "<one sentence: what check.py is actually asserting>"
  failure_pattern: "<hard only: one sentence explaining what browser-use gets wrong>"
  primary_track: true
  tier: <3 hard | 2 medium | 1 easy>
```

The `agent_interaction` and `checks_verify` fields document *why* the task
belongs at its difficulty level — fill them in thoughtfully.

### seed.py critical rules
- **Always cleanup prior runs first**
- Use correct Odoo 19 field names: `tax_ids` (not `tax_id`), `group_ids` (not
  `groups_id`), `memo` (not `ref` on payment), `product_qty` (not `quantity`
  on PO line)
- Enable required features: credit limits via `ir.config_parameter`, discount
  groups via `sale.group_discount_per_so_line`
- Clear taxes with `"tax_ids": [(5, 0, 0)]` if prompt quotes exact untaxed totals
- Set `invoice_policy: "order"` on products for invoicing tasks
- Use `supplier_rank: 1` for vendor partners

### expected_state.json rules
- Only include **actual state changes** (not unchanged values)
- Entity keys come from state_spec match_key fields, normalized: Many2one →
  display name, False → null
- Use `"op": "set"` for changes, `"op": "create"` for new records
- **Never use `"op": "eq"`, `"domain"`, or `"__count__"`** — unsupported
- Keep it minimal — validate details in check.py instead
- **Pro tip**: Run once, check `state_diff.json` artifact for real entity keys

### check.py rules
This is the most important validation file. Validate according to difficulty:

- **Hard**: exact line-item values, distractor records untouched, wizard choice
  implicit in final state, record counts, specific field values across records
- **Medium**: primary record state, 1-2 key fields, no extra/missing records,
  one workflow action completed
- **Easy**: single field value or state change; optionally a linked record

### trace_spec.yaml rules
- Put wizard action methods in `required_ops` (e.g., `refund_moves`,
  `action_create_payments`)
- Put `create`/`write`/`web_save` in `optional_ops` (browser uses `web_save`
  instead of ORM methods)
- Put destructive operations in `forbidden_ops` (`unlink`, `button_cancel`, etc.)

---

## Step 4: Check if required modules are installed

```bash
psql -tAc "SELECT name FROM ir_module_module WHERE state='installed' AND name='<module>'" benchmark_validate
```

If not installed:
```bash
.venv/bin/python3 odoo-bin -d benchmark_validate -i <module> -c .odoorc.local --stop-after-init
PYTHONPATH=. python benchmark/eval.py prepare-base --db benchmark_validate
```

---

## Step 5: Test as human first

```bash
PYTHONPATH=. python benchmark/eval.py run <task_name> --agent human
```

Verify:
- Seed runs without errors (no `WARNING: seed may have failed`)
- You can complete the task following prompt.md exactly
- Postconditions pass (empty `[]`)

---

## Step 6: Run against browser-use

```bash
PYTHONPATH=. python benchmark/eval.py run <task_name> --agent browser-use
```

**Always headed mode** (default). Never `--headless`.

Interpret the result against the target pass rate for the difficulty:

| Result | Hard | Medium | Easy |
|--------|------|--------|------|
| `FAIL + postcondition failures` | Good (expected) | Good | Acceptable — task is harder than intended, keep it |
| `PASS` | Too easy — add harder pattern | Expected ~60% | Expected ~80% |
| `FAIL + empty postconditions` | Diff engine mismatch — fix entity keys | Same | Same |
| `seed may have failed` | Fix field names in seed.py | Same | Same |

Run at least **twice** to confirm consistency. If a hard task passes consistently,
go back to Step 0 and reconsider the difficulty level or add a harder interaction
pattern. If an easy or medium task fails consistently, that is acceptable —
**do not simplify the task to make it pass**. A task harder than its tier is
fine; a task easier than its tier is not.

### Diagnosing failures: agent capability vs. task design

A `FAIL` result can mean two very different things. You must distinguish them
before deciding whether to fix anything:

**Agent capability failure** — the agent understood the task and attempted the
right workflow, but made a mistake (wrong record, bad field value, missed a
wizard step). This is expected and desirable for hard tasks.

Signs: agent navigated to the right module, took plausible actions, but
postconditions failed on a specific value or state.

**Task design failure** — the task itself is broken, so even a capable agent
could not succeed. These MUST be fixed regardless of difficulty tier.

Signs and fixes:

| Symptom | Root cause | Fix |
|---------|-----------|-----|
| Agent never finds the right record | Prompt names don't match seed data | Align prompt and seed |
| Agent follows prompt exactly but postconditions fail | `expected_state.json` wrong | Fix expected values |
| Agent tries a workflow the UI doesn't support | Prompt describes non-existent button/flow | Fix prompt to match real UI |
| Agent succeeds but check.py fails | `check.py` checks wrong model/field | Fix check.py |
| Seed error in logs | Incorrect field names in seed.py | Fix seed field names |
| Agent skips a required step | Prompt is ambiguous — step not clearly required | Clarify prompt |

**How to tell them apart**: watch the browser-use recording. If the agent
clearly attempted the correct workflow and was defeated by Odoo's complexity,
that is capability. If the agent was confused about what to do or where to go,
that is task design.

---

## Step 7: Cross-review (MANDATORY — never self-review)

**You must get a second opinion from a DIFFERENT model.** Self-review misses
the same blind spots that produced the bugs.

- **If you are Claude Code**: delegate the review to Codex via `codex:rescue` agent
- **If you are Codex**: hand the files back to Claude Code for review

The reviewer checks: A. Instruction clarity, B. Doability, C. Timeout adequacy,
D. Seed-prompt consistency, E. Expected state correctness, F. check.py
correctness, G. trace_spec correctness, **H. Difficulty calibration** — does
the task actually require the interactions its difficulty level implies?

Fix any blocking issues, then re-run against browser-use.

---

## Step 8: Update STATUS.md and commit

Update the task's row from `WIP` to `Done` and fill in the test results.
Include difficulty in the description column so the table is self-documenting:

```markdown
| N | <task_name> [<difficulty>] | <description> | Done | PASS | FAIL/PASS | <F1> |
```

Only mark `Done` if ALL of these are true:
- [ ] Seed runs without errors
- [ ] Human can complete the task (oracle passes)
- [ ] Browser-use result is consistent with the target pass rate for the level
- [ ] Failure (hard) or pass (easy) is genuine, not a diff-engine mismatch
- [ ] Cross-review passed (no blocking issues)
- [ ] Task doesn't duplicate an existing task's workflow

Then commit and push:
```bash
git add benchmark/tasks/<task_name>/ benchmark/tasks/STATUS.md
git commit -m "[ADD] benchmark: <task_name> task (<difficulty>)"
git push upstream odoo_benchmark
```
