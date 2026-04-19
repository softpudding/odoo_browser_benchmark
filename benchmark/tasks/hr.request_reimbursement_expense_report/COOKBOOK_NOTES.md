# Odoo 19 quirks discovered in hr.request_reimbursement_expense_report

Context: STATUS row 465. The task walks a single `hr.expense` through the
full Draft → Submitted → Approved → Posted lifecycle. Row 368's cookbook
had already confirmed that `hr.expense.sheet` is removed in Odoo 19; this
task consolidates the *reimbursement* pathway (admin posting their own
employee-paid expense) and surfaces a few additional traps.

## Admin submitting their own expense auto-validates

`hr.expense._can_be_autovalidated` returns True when:

  (not self.manager_id and not self.employee_id.expense_manager_id)
  OR self.manager_id == self.employee_id.user_id

If admin is both the employee and has no `expense_manager_id` on their
own `hr.employee` record, `action_submit` calls `_do_approve(check=False)`
internally and the expense jumps from `draft` straight to `approved`,
collapsing the 3-step workflow into 1. To preserve the Submit → Approve
separation while still letting admin approve, seed a dedicated
`bench_expense_manager` user + employee and set:

```python
admin_emp.write({"expense_manager_id": manager_user.id})
```

Admin still has `can_approve=True` on the resulting submitted expense
because `_get_cannot_approve_reason` short-circuits the "own expense"
check when the approver has `group_hr_expense_manager`
(`is_hr_admin=True`).

## Post Journal Entries gating

The statusbar button `name="action_post"` with label "Post Journal
Entries" is only visible when:

  * `state == 'approved'`, AND
  * user in `account.group_account_invoice`

Granting only the three `hr_expense.*` groups is NOT enough. Seed must
add `account.group_account_invoice` to admin:

```python
for grp_ref in [
    "hr_expense.group_hr_expense_user",
    "hr_expense.group_hr_expense_team_approver",
    "hr_expense.group_hr_expense_manager",
    "account.group_account_invoice",
]:
    group = env.ref(grp_ref, raise_if_not_found=False)
    if group and group not in admin.group_ids:
        admin.write({"group_ids": [(4, group.id)]})
```

## hr.expense.post.wizard primary button

The wizard opened by `action_post` is `hr.expense.post.wizard`. Footer:

```xml
<button name="action_post_entry" string="Post Expenses" type="object"
        class="oe_highlight" data-hotkey="q"/>
```

Oracle selector that works across browser versions:

```python
page.locator(".o_dialog:visible button[name='action_post_entry']")
```

The wizard has two pre-filled fields (Employee Journal default is a
purchase-type journal; Accounting Date = today). Do NOT touch them — the
prompt's "accept defaults" contract fails silently if the agent edits
them because different companies' default purchase journals are
indistinguishable in the state diff.

## hr.expense.state='posted' is the v19 equivalent of "Expense Report Done"

`_compute_state` in hr.expense.py:

```python
if move.state == 'cancel':
    expense.state = 'paid'   # yes, weird
else:
    if move.payment_state == 'paid':
        expense.state = 'paid'
    elif move.state == 'draft':
        expense.state = 'posted'
    elif move.payment_state == 'not_paid':
        expense.state = 'posted'
    ...
else:
    expense.state = expense.approval_state or 'draft'
```

So right after `hr.expense.post.wizard.action_post_entry` runs, the
account.move is `posted` with `payment_state='not_paid'` and the expense
rolls up as `state='posted'`, `approval_state='approved'`. That's the
canonical final state for a fully-processed reimbursement request —
tasks ported from pre-v19 that say `sheet.state='done'` should target
`hr.expense.state='posted'` instead.

## state_spec match_key for a single expense

With `match_key=[name]`, the entity_key normalizes to a single string:
`["Bench Travel Expense"]` (not a tuple). Since the record existed in
before_state (seeded as draft), the two tracked transitions are
`op=set` not `op=create`:

```json
{"field": "state", "op": "set", "norm_value": "posted"}
{"field": "approval_state", "op": "set", "norm_value": "approved"}
```

`account_move_id` is in ignore_fields because the move's id is
run-specific. Move existence + posted-state is validated in check.py.

## Calibration: reimbursement lifecycle is too easy for BU

Empirically the 4-click lifecycle (click row → Submit → Approve → Post
Journal Entries → Post Expenses) is solved by browser-use single-shot
in ~74s / 11 steps, F1=1.0. It's not a hard-tier failure pattern on its
own. To actually make this hard:

  * Add the duplicate-approve wizard (seed a duplicate expense the
    agent must dismiss with "Approve Anyway" vs "Back"),
  * Require a non-default Journal in the Post Expenses wizard (BU
    defaults-accepts),
  * Combine with attachment upload (BU's available_file_paths sandbox
    issue — see row 464 notes).

Kept at tier 3 for pathway coverage (no other task in the bench walks
the full reimbursement lifecycle end-to-end), flagged `primary_track:
true` so it contributes to F1-vs-difficulty calibration curves even
though BU passes it.
