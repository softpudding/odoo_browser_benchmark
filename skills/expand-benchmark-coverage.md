---
name: expand-benchmark-coverage
description: Guide for creating benchmark tasks in under-covered Odoo modules. Shows which modules lack tasks, which are ready to use, and which need installation first. Pair with /create-benchmark-task to actually build the task.
user-invocable: true
argument-hint: [module_name] or blank to see the coverage map
---

# Expand Benchmark Coverage to Missing Odoo Modules

This skill helps you identify and fill gaps in the benchmark task suite. Use it
BEFORE `/create-benchmark-task` to pick a high-value target module and workflow.

---

## Step 0: If a specific module was requested

If `$ARGUMENTS` names a module (e.g. `mrp`, `pos`, `website_sale`), skip to
**Step 2** for that module. Otherwise, show the user the coverage map below.

---

## Step 1: Coverage map — where the gaps are

Read `benchmark/tasks/STATUS.md` and count tasks per module. Then present this
table, updated with live counts:

### Well-covered (10+ tasks) — deprioritize unless the user has a specific workflow

| Module | Odoo app | Approx. tasks |
|--------|----------|---------------|
| `account` | Accounting | ~15 |
| `crm` | CRM | ~12 |
| `sale` | Sales | ~14 |
| `purchase` | Purchase | ~10 |
| `project` | Project | ~12 |
| `hr` / `hr_recruitment` | HR / Recruitment | ~12 |

### Lightly covered (1–6 tasks) — good candidates for more variety

| Module | Odoo app | Approx. tasks | What's missing |
|--------|----------|---------------|----------------|
| `stock` | Inventory | ~6 | Scrap wizard variants, putaway rules, lot/serial tracking, inventory adjustments with locations |
| `calendar` | Calendar | ~6 | All-day events, multi-attendee management, video call links |
| `contacts` | Contacts | ~8 | Merge contacts, archive/unarchive, bank account management |
| `website` | Website | ~4 | Blog posts, form builder, menu editing, SEO settings, multi-page editing |

### ZERO coverage — highest priority for new tasks

These modules represent major Odoo functionality with no benchmark tasks at all.
They are grouped by installation readiness:

#### Ready to use (already installed in base snapshot)

No changes to `base_modules.txt` needed. Just write tasks.

| Module | Odoo app | Why it matters | Example workflows |
|--------|----------|---------------|-------------------|
| `hr_holidays` | Time Off | Core HR workflow, approval chains | Request leave, approve/refuse, allocate days |
| `hr_expense` | Expenses | Receipt upload, approval, payment | Create expense report, attach receipt, submit for approval |
| `mail` | Discuss | Internal messaging, channels | Create channel, send message, pin conversation |
| `mrp` | Manufacturing | Core ERP pillar, unique BOM/MO UI | Create BOM, confirm manufacturing order, record production |
| `website_sale` | E-Commerce | Public storefront, cart/checkout | Add product to shop, configure variants, process order |
| `point_of_sale` | POS | Full-screen kiosk UI, completely different paradigm | Open session, ring up sale, process payment, close session |
| `im_livechat` | Live Chat | Real-time chat widget, WebSocket-based | Create channel, set canned responses, handle chat session |
| `fleet` | Fleet | Vehicle management | Add vehicle, log odometer, manage contracts |
| `event` | Events | Event management, registration | Create event, manage tickets, track registrations |

#### Enterprise-only (not available in Community Edition)

These modules cannot be installed — skip them for benchmark tasks.

| Module | Odoo app |
|--------|----------|
| `appointment` | Appointments |
| `marketing_automation` | Marketing Automation |
| `helpdesk` | Helpdesk |

#### Caution — installed but may need infra adaptation

| Module | Issue | Recommendation |
|--------|-------|----------------|
| `point_of_sale` | Full-screen kiosk UI is not standard Odoo backend; browser agent may need different navigation patterns | Spike first: try one manual task, see if eval harness captures traces correctly |
| `im_livechat` | Real-time WebSocket chat may not play well with trace-based evaluation | Spike first: check if `benchmark_trace` captures chat actions |

---

## Step 2: Suggest concrete task ideas for the chosen module

Once the user picks a module (or you're working from `$ARGUMENTS`), propose
3-5 task ideas across difficulty levels. For each, describe:

1. **Task name** — `module.descriptive_action` format
2. **Difficulty** — easy / medium / hard, with reasoning
3. **Workflow** — 1-2 sentence description of what the agent does
4. **Capability tested** — what browser interaction pattern this exercises
5. **Overlap check** — confirm it's distinct from existing tasks on 2+ of 3
   dimensions (module, workflow type, capability tested)

Prefer workflows that exercise Odoo UI patterns NOT already well-tested:
- Approval/refusal chains (Time Off, Expenses)
- Kiosk/full-screen interfaces (POS)
- Public-facing portals (E-Commerce, Appointments)
- Drag-and-drop or canvas interactions (Manufacturing BOM editor)
- Multi-level wizards with conditional steps

---

## Step 3: Check module installation (BEFORE worktree)

**This step MUST happen on the main project, not in a worktree.** The base
snapshot is shared infrastructure — `base_modules.txt`, the installed module
list, and the snapshot dump are used by ALL tasks. `/create-benchmark-task`
enters a worktree later for task-specific files, but module installation and
snapshot rebuilding must be done first on the main branch.

Verify the module is installed:

```bash
psql -tAc "SELECT name FROM ir_module_module WHERE state='installed' AND name='<module>'" benchmark_validate
```

If not installed:
1. Add to `benchmark/base_modules.txt` (main branch)
2. Install and rebuild the snapshot:
   ```bash
   .venv/bin/python3 odoo-bin -d benchmark_validate -i <module> -c .odoorc.local --stop-after-init
   PYTHONPATH=. python benchmark/eval.py prepare-base --db benchmark_validate
   ```
3. Spot-check 2-3 existing tasks to confirm the rebuild didn't break anything:
   ```bash
   PYTHONPATH=. python benchmark/eval.py run sale.change_validity_date --agent human
   PYTHONPATH=. python benchmark/eval.py run crm.move_opportunity_stage --agent human
   ```
4. Commit and push the `base_modules.txt` change:
   ```bash
   git add benchmark/base_modules.txt
   git commit -m "benchmark: add <module> to base snapshot modules"
   git push
   ```

Only after the module is installed and the snapshot is rebuilt, proceed to
`/create-benchmark-task` (which will enter its own worktree for task files).

---

## Step 4: Hand off to /create-benchmark-task

Once the module is installed and the user has chosen a specific task, run:

```
/create-benchmark-task <module.task_name> <difficulty>
```

That skill handles worktree entry, file creation, testing, and validation.
The module installation from Step 3 is already on the main branch, so the
worktree will inherit it.

---

## Quick-win suggestions (copy-paste ready)

If the user just wants to start filling gaps immediately, here are pre-designed
tasks for the highest-priority missing modules. Each is ready to hand to
`/create-benchmark-task`:

### Manufacturing (`mrp`) — ready to use

```
/create-benchmark-task mrp.create_bom_confirm_mo medium
```
Create a Bill of Materials for a product with 3 components, then create and
confirm a Manufacturing Order for 10 units.

```
/create-benchmark-task mrp.produce_and_close_mo medium
```
Open a confirmed MO, record production quantities on each component, and mark
the MO as done.

### E-Commerce (`website_sale`) — ready to use

```
/create-benchmark-task website_sale.publish_product_set_price medium
```
Open a product in the website shop editor, set its published price and
description, and toggle it to Published.

### Time Off (`hr_holidays`) — ready to use

```
/create-benchmark-task hr_holidays.request_leave_approve medium
```
As employee, request 3 days of Annual Leave. Switch to manager view and approve.

```
/create-benchmark-task hr_holidays.allocate_leave_days easy
```
Allocate 15 days of Sick Leave to an employee.

### Expenses (`hr_expense`) — ready to use

```
/create-benchmark-task hr_expense.create_expense_report_submit medium
```
Create an expense line for a hotel stay, attach it to a new expense report,
and submit for approval.
