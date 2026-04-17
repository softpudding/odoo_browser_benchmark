---
name: write-oracle-solution
description: Write or fix a Playwright oracle script (oracle.py) for a benchmark task. The oracle proves the task is solvable through the browser UI. Debugs against the running Odoo instance, fixes selectors, and verifies via eval.py --agent oracle. Use when a task needs an oracle script or an existing one is failing.
user-invocable: true
argument-hint: [task_name]
---

# Write an Oracle Solution for a Benchmark Task

You are writing or fixing a Playwright oracle script for the benchmark task
`$ARGUMENTS`. The oracle proves this task is solvable through the browser UI —
it is the gold-standard solution.

## WORKTREE REQUIREMENT

**You MUST work in a separate git worktree for this skill.** Before doing any
file reads or edits, use `EnterWorktree` to create a new worktree. All oracle
development (editing oracle.py, debugging, running eval) happens inside the
worktree. Only exit the worktree (which merges changes back) once the oracle
passes or you are done.

## CRITICAL RULES

1. **NEVER lower task difficulty.** The oracle must solve the task the same way
   a browser agent would — navigating the UI, reading visible information,
   clicking buttons, using the search bar. Do NOT hardcode shortcuts that bypass
   UI challenges. If the task says "find the invoice by origin VAT-302" and the
   origin isn't in a visible column, use the search bar — that's what a real
   agent would do.

2. **Never modify prompt.md to make things easier.** If the prompt describes a
   hard workflow, the oracle must follow it. Consult the user before changing
   any task specification files.

3. **Fix real bugs only.** You may fix expected_state.json if it has arithmetic
   errors, missing fields tracked by state_spec.yaml, or values that don't
   match what Odoo actually produces. These are legitimate spec bugs, not
   difficulty reductions.

---

## Step 1: Understand the task

Read all task files:
```
cat benchmark/tasks/$ARGUMENTS/prompt.md
cat benchmark/tasks/$ARGUMENTS/seed.py
cat benchmark/tasks/$ARGUMENTS/task.yaml
cat benchmark/tasks/$ARGUMENTS/state_spec.yaml
cat benchmark/tasks/$ARGUMENTS/expected_state.json
cat benchmark/tasks/$ARGUMENTS/check.py
```

Understand: what does the agent need to do? What data does the seed create?
What state changes are expected?

---

## Step 2: Read or create the oracle script

```
cat benchmark/tasks/$ARGUMENTS/oracle.py 2>/dev/null || echo "No oracle yet"
```

The oracle script must follow this structure:

```python
"""Oracle for $ARGUMENTS."""

from benchmark.oracle_helpers import (
    login,
    navigate,
    run_oracle,
    # ... import only what you need
)


def oracle(page):
    login(page)
    navigate(page, "/odoo/...")
    # ... complete the task via Playwright
    

run_oracle(oracle)
```

---

## Step 3: Debug interactively

Use this pattern to explore the Odoo UI DOM:

```python
import os
os.environ.update({
    'BENCHMARK_BASE_URL': 'http://127.0.0.1:8069',
    'BENCHMARK_DB': 'benchmark_validate',
    'BENCHMARK_LOGIN': 'admin',
    'BENCHMARK_PASSWORD': 'admin',
    'BENCHMARK_HEADED': '1',
})
import benchmark.oracle_helpers as oh

with oh.odoo_browser() as page:
    oh.login(page)
    oh.navigate(page, '/odoo/sales')
    oh._wait_no_loading(page)
    page.wait_for_timeout(2000)
    
    # Explore DOM elements:
    btns = page.locator('button:visible')
    for i in range(btns.count()):
        txt = btns.nth(i).inner_text().strip()
        name = btns.nth(i).get_attribute('name') or ''
        if txt:
            print(f'  Button: "{txt}" name={name}')
```

Run with: `PYTHONPATH=. python /tmp/debug_script.py`

---

## Step 4: Odoo 19 UI reference

### Navigation & Views
- `/odoo/sales` — Sales (list view, has "My Quotations" filter)
- `/odoo/purchase` — Purchase orders
- `/odoo/accounting/customer-invoices` — Invoice list (NOT `/odoo/accounting` which shows dashboard)
- `/odoo/crm` — CRM pipeline (kanban). Leads: `/web#action=crm.crm_lead_all_leads`
- `/odoo/calendar` — Calendar view
- `/odoo/project` — Projects (kanban)
- `/odoo/recruitment` — Recruitment (kanban)
- `/jobs` — Public job listings (no login needed)

### Login
- `login(page)` handles the login form
- For public tasks (login: null in task.yaml), do NOT call login()

### List view
- `click_list_row(page, text)` — auto-clears filters, auto-searches via search bar, clicks first match
- `clear_search_filters(page)` — removes "My Quotations" etc.
- `ensure_list_view(page)` — switches from kanban to list

### Forms
- `fill_field(page, field_name, value)` — char/integer fields with `<input>`
- `fill_text_field(page, field_name, value)` — `<textarea>` fields
- `set_many2one(page, field_name, search_text)` — many2one dropdown
- `set_date(page, field_name, "MM/DD/YYYY")` — date fields (handles button-based picker)
- `set_boolean(page, field_name, True/False)` — checkboxes
- `add_many2many_tag(page, field_name, tag_text)` — tags
- `click_tab(page, "Other Info")` — notebook tabs
- `save_form(page)` — save button
- `click_status_button(page, "Confirm")` — statusbar buttons

### One2many lines (order lines, invoice lines)
- `click_add_a_line(page)` — "Add a product" / "Add a line"
- `set_o2m_field(page, row_idx, field_name, value)` — edit inline field
- `set_o2m_many2one(page, row_idx, field_name, text)` — set product in line
- Sale order lines: product field is `product_template_id`
- Purchase order lines: product field is `product_id`
- Invoice lines: qty field is `quantity`

### Modals / Wizards
- `modal_click_button(page, "Reverse")` — button in modal
- `modal_fill_field(page, field_name, value)` — field in modal
- `modal_set_many2one(page, field_name, text)` — many2one in modal
- `modal_set_date(page, field_name, "MM/DD/YYYY")` — date in modal (handles button→input)

### Action menu
```python
page.locator(".o_cp_action_menus .dropdown-toggle").first.click()
page.wait_for_timeout(500)
page.locator(".dropdown-menu:visible .dropdown-item").filter(has_text="Duplicate").first.click()
```

### Chatter / Activities
- `schedule_activity(page, activity_type="Call", summary="...", due_date="MM/DD/YYYY", assigned_to="Name")`
- Activity type uses selection badges (clickable badges, not dropdown)
- Activity button: `button.o-mail-Chatter-activity`

### Calendar
- Scale dropdown: `.scale_button_selection` → `.dropdown-item:has-text("Week")`
- Navigation: `.o_calendar_button_next`, `.o_calendar_button_prev`
- Events: `.fc-event`; click → popover with `a.o_cw_popover_edit`
- Recurrence dialog: inline radio `data-value="self_only"` (not a modal)

### Project kanban
- Kebab menu: hover card → `.o_dropdown_kanban .dropdown-toggle`
- Settings: `.dropdown-item:has-text("Settings")`

### Website editor
- Opens via `?enable_editor=1` on any website page
- Content may be in an iframe — use `page.frame_locator("iframe")`
- Navbar may be hidden (`display:none`) during editing
- Save: `button[data-action='save']`
- Page properties: via Site menu in the navbar

### Key gotchas
- `wait_for_load_state("networkidle")` NEVER works (Odoo longpoll). Use `"load"` or `wait_for_timeout`.
- Tooltips can intercept clicks — `_dismiss_tooltips(page)` removes them
- Date fields use button-based pickers, NOT text inputs
- `Escape` key can close modals — only press if a datepicker is actually open
- Cancel buttons on SO/PO trigger `ConfirmationDialog` (Odoo modal, not browser dialog)
- Optional columns (like Disc.%) need `enable_optional_column(page, "Disc")` to show

---

## Step 5: Run and verify

```bash
uv run benchmark-eval run $ARGUMENTS --agent oracle
```

Check the output:
- **RESULT: PASS** — done!
- **Oracle: FAIL** — Playwright error, fix the selector/logic
- **Oracle: PASS but RESULT: FAIL** — state mismatch. Check:
  ```bash
  dir=$(ls -td benchmark/reports/runs/$ARGUMENTS__oracle__* | head -1)
  cat $dir/postcondition_failures.json
  cat $dir/state_diff.json
  cat $dir/expected_state.json
  cat $dir/score.json
  ```

### Common fixes for state mismatch
- `expected_state.json` missing fields tracked by `state_spec.yaml`
- `expected_state.json` has wrong arithmetic
- `trace_spec.yaml` has wrong op names (Odoo 19 uses `web_save` not `write`)
- `check.py` checks something the oracle doesn't produce

---

## Step 6: Validate you haven't lowered difficulty

Before finishing, review your changes:
- Did you change `prompt.md`? → Consult user first
- Did you change `expected_state.json`? → Only for legitimate bugs (math errors, missing fields)
- Did you change `state_spec.yaml`? → Only if it tracks wrong fields
- Did you change `check.py`? → Only if it checks impossible conditions

The oracle proves the task IS solvable. It must NOT make the task easier for
browser agents.
