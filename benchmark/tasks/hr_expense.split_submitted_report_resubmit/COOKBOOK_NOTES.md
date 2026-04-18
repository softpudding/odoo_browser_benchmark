# Odoo 19 quirks discovered in hr_expense.split_submitted_report_resubmit

## hr.expense.sheet — definitively gone, no per-line refuse, no auto-split

Confirmation for STATUS row 368: the legacy `hr.expense.sheet` "Expense
Report" wrapper is removed in Odoo 19. There is **no** "refuse one line,
others stay in the sheet" behaviour, and there is **no** "Split action"
on a sheet that splits the refused line into a new sheet. The canonical
approval loop in Odoo 19 is directly on `hr.expense` with
`approval_state` ∈ `{submitted, approved, refused}` and a computed
`state` that mirrors it plus posted/paid.

Any task from an older spec that assumes sheets must be redesigned as a
batch of individual `hr.expense` records sharing a naming convention.

## Refuse wizard = `hr.expense.refuse.wizard`

Clicking **Refuse** on the form statusbar opens the wizard returned by
`hr.expense.action_refuse` → xmlid
`hr_expense.hr_expense_refuse_wizard_action`. The wizard has one
required field `reason` (Char) and an `action_refuse` method that calls
`_do_refuse(reason)` on the source expense(s). The reason is posted to
the chatter via the `hr_expense.hr_expense_template_refuse_reason`
mail template — check.py should grep `m.body` on `expense.message_ids`.

The wizard **does not** auto-close its modal after submit — oracle code
should click the primary button in the modal then wait for the modal to
disappear before navigating back.

## Approver visibility requires three groups

To see both **Approve** and **Refuse** on another employee's submitted
expense, the admin/approver must be in all of:

- `hr_expense.group_hr_expense_user`
- `hr_expense.group_hr_expense_team_approver`
- `hr_expense.group_hr_expense_manager`

Base snapshot doesn't grant the team_approver group to admin by
default. Seed pattern:

```python
for grp_ref in [
    "hr_expense.group_hr_expense_team_approver",
    "hr_expense.group_hr_expense_manager",
    "hr_expense.group_hr_expense_user",
]:
    group = env.ref(grp_ref, raise_if_not_found=False)
    if group and group not in admin.group_ids:
        admin.write({"group_ids": [(4, group.id)]})
```

Additionally, the employee being approved needs `expense_manager_id`
set to the approver user so `_get_default_responsible_for_approval`
resolves correctly; otherwise submits to that employee drop straight
into an auto-validated path or miss the approver queue.

## Approver list action xmlid

The "all expenses" manager list (spanning employees) is
`hr_expense.hr_expense_actions_my_all` — reachable via
`/odoo/action-hr_expense.hr_expense_actions_my_all`. Plain
`/odoo/expenses` opens the current user's **My Expenses** kanban, which
on admin only shows admin's own expenses; Lee Bench's submitted records
are invisible from that view. Oracles that need to open another
employee's expense should start from `/odoo/expenses` for the URL
match, then navigate to the xmlid action.

## BU passes "refuse one + approve two" loops in ~140s

Calibration note: a 3-expense triage loop (refuse one with wizard
reason, approve the remaining two individually) is NOT a hard-tier
failure pattern against browser-use — BU solved it F1=1.0 on first
shot in 143.4s (single-shot, no retries). Pure multi-record loops
without wizards-with-non-default-radios or create-from-scratch do not
reliably trip BU. If you want to re-tier this pattern upward, add a
non-default selection somewhere (e.g., require a specific reason from a
dropdown instead of free text, or combine with a split wizard that
forces a non-default amount allocation).
