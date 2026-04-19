# hr_holidays.request_sick_leave_approve_self - Odoo 19 quirks

## `hr.leave.action_confirm` does NOT exist in Odoo 19

Unlike older Odoo versions, `hr.leave` in Odoo 19 does not expose an
`action_confirm` method. The lifecycle API surface on `hr.leave` is:

```
action_approve      (confirm -> validate)
action_back_to_approval  (validate -> confirm)
action_refuse       (any -> refuse)
action_cancel       (limited set -> cancel)
action_documents
```

There is no `action_confirm`. The `state` field declares
`default='confirm'`, so a fresh `create()` lands in `confirm` immediately.
Oracles that call `.create()` then `.action_confirm()` fail with
`AttributeError: The method 'hr.leave.action_confirm' does not exist` —
just drop the confirm call.

The view does NOT render a "Submit" button either, because there's no
`draft` -> `confirm` transition needed. The form saves to `confirm`.

## `hr.leave.type.requires_allocation` is a `fields.Boolean` in this build

Despite what `hr_holidays.request_allocation_approve_self_book_day_off`'s
cookbook claims (`"yes"`/`"no"` Selection), in this Odoo 19 build
`hr.leave.type.requires_allocation` is declared at:

```python
# addons/hr_holidays/models/hr_leave_type.py:88
requires_allocation = fields.Boolean(default=True, required=True, string='Requires allocation')
```

Seed with `False` / `True`, not `"no"` / `"yes"`. Passing `"yes"` / `"no"`
happens to coerce to truthy and works for most flows, but explicit booleans
are safer. When `True`, `_check_validity` fires on `.create()` and raises
`"You do not have any allocation for this time off type."` — this is the
same trap the allocation task warns about, just triggered from a seed-level
misconfig.

`Sick Leave` in the benchmark base snapshot ships with
`requires_allocation=True`. Our seed flips it to `False` so a sick day
can be booked without a prior allocation.

## `leave_validation_type='hr'` vs the admin approver

`leave_validation_type` governs the Approve lifecycle:

- `no_validation` — approves on confirm
- `manager` — employee's leave_manager_id approves; state goes
  `confirm` -> `validate`
- `hr` — requires an HR / Time Off Officer (group
  `hr_holidays.group_hr_holidays_user`); state `confirm` -> `validate`
- `both` — requires manager then HR; state
  `confirm` -> `validate1` -> `validate`

For this task we use `'hr'`. The seed grants admin the
`hr_holidays.group_hr_holidays_user`, `group_hr_holidays_manager`, and
`group_hr_holidays_responsible` groups so admin has authority to approve
any pending request from the Management dashboard. Without those groups
`action_approve` RPCs from the admin session raise an access-rights error.

## `number_of_days` is working-day based, not calendar days

`hr.leave.number_of_days` is computed against the employee's resource
calendar (default = Mon–Fri working week). A `date_from=2026-05-10
date_to=2026-05-11` request (Sunday -> Monday) yields `number_of_days=1.0`,
not 2.0, because Sunday is a non-working day.

We use **2026-05-11 (Monday) -> 2026-05-12 (Tuesday)** instead, which
cleanly yields `number_of_days=2.0` and makes the state-diff expectation
deterministic. If you keep a weekend-straddling range, drop
`number_of_days` from `state_spec.yaml` or pin it to the true working-day
count.

## `hr.leave.state_spec` `match_key` with two many2ones

This task tracks `hr.leave` by `match_key: [employee_id, holiday_status_id]`
so the diff engine reliably identifies the single approved leave. Both
normalize to their Many2one display names (`"Bench Sick Employee"` and
`"Sick Leave"`). Do NOT include `name` as a match key — `hr.leave.name` is
a free-text description that browser-use often leaves blank or garbled, so
the match becomes `[... , null]` and diverges from the expected entity
key.

## State-diff `op: create` for the new leave

Since this task creates an `hr.leave` from scratch (no pre-existing record
with that employee + type), every diff row for the new record comes back as
`op: "create"`, including `state`. Use:

```json
{"op": "create", "field": "state", "norm_value": "validate"}
```

rather than `"op": "set"`. Mixing `set` and `create` on a brand-new record
tanks F1.

## Browser-use failure mode (calibration)

In a single-shot run, browser-use exhausted the 420s limit stuck in the
new-request form. It:

- Left the date_from/date_to fields at today (the `2026-04-19` default)
  rather than picking 2026-05-11/2026-05-12 through the datetime widget.
- Never reached the Management / Approvals dashboard — so
  `action_approve` was never called and the leave stayed in `confirm`.

Result: `Strict FAIL`, F1=0.0, RequiredOpRecall=0.0. The date-picker +
two-step role lifecycle combination lives up to the hard-tier calibration.
