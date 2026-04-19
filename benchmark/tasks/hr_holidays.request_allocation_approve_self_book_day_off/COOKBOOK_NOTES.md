# hr_holidays.request_allocation_approve_self_book_day_off - Odoo 19 quirks

## `hr.leave.type.requires_allocation` is a Selection, not Boolean

In Odoo 19 `hr.leave.type.requires_allocation` is a Selection field with
values `'yes'` / `'no'`, NOT a boolean. Seeding with `True` works on some
legacy snapshots but will break schema validation on a clean base. Use the
string:

```python
env["hr.leave.type"].create({
    "name": "Bench Bonus Days",
    "requires_allocation": "yes",
    "allocation_validation_type": "officer",
    ...
})
```

## Allocation validation Confirm -> Approve lifecycle

With `allocation_validation_type='officer'` an allocation starts in
`confirm` on `create()` via the default; callers must still invoke
`action_confirm()` (no-op if already in confirm) then `action_approve()`
to reach `validate`. From the UI:

- "New" -> Save -> draft
- Click "Confirm" (if the button is visible) -> `confirm`
- Click "Approve" -> `validate`

Some create flows skip the separate Confirm button and go straight from
draft to `confirm` via a default; the Approve click alone is then enough.
Our oracle defensively calls `action_confirm` before `action_approve` -
`action_confirm` on an already-confirmed record is a no-op.

## Order matters: allocation must validate before leave

`hr.leave.type.requires_allocation='yes'` makes `hr.leave` with that type
check the virtual remaining leaves in its onchange / `_check_holidays`
server-side constraint. Creating + approving the leave BEFORE the
allocation is in `validate` state fails with
"The number of remaining time off is not sufficient for this time off
type." BU commonly tries to do the second phase first and gets stuck here.

## `parent_id` on hr.employee vs `leave_manager_id`

- `parent_id` = department / reporting tree parent (for "My Team" filters).
- `leave_manager_id` = who approves the employee's time off.

Seed both when you want admin to be both the approver AND show up in
"Waiting For Me" filter; seeding only `parent_id` does NOT make admin the
approver.

## State-diff `op: create` for newly created records

Because this task is a clean create-from-scratch (no pre-existing
allocation / leave), the state-diff shows `op: create` entries for every
tracked field. In `expected_state.json` use:

```json
{"op": "create", "field": "state", "norm_value": "validate"}
```

rather than `"op": "set"`. Using `"op": "set"` on a new record will show
as an extra/missed op in the diff and tank F1.
