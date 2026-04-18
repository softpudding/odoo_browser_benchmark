# hr_holidays.bulk_approve_two_pending_requests — Odoo 19 quirks

## `hr.leave` list view bulk Approve is NOT in the cog Actions menu

The Time Off manager list view (`hr_leave_view_tree`, used by
`/odoo/time-off-approval`) declares `js_class="hr_holidays_payslip_list"`.
The controller in
`addons/hr_holidays/static/src/views/list/holidays_list_controller.js`
registers a custom `HolidaysListController` that:

- Reads the view-level `<header><button name="action_approve">` /
  `<button name="action_refuse">` declarations,
- Filters the selected records through `displayButton()` so only
  selections containing ≥1 `can_approve`/`can_validate` record show the
  Approve button,
- Renders those buttons in the control-panel **selection-actions** slot
  (`control-panel-selection-actions`) — NOT under the generic cog
  "Actions" menu.

Practical consequences for oracle authors:

- Locator for the bulk Approve button after selection:
  `.o_control_panel button[name='action_approve']:visible` works reliably.
  (There is NO `dropdown-item:has-text('Approve')` entry in the cog menu
  for `hr.leave` on this view.)
- `action_approve` is called via `ORM.call(..., [record_ids])` which
  approves all selected records in one round trip — this is what makes
  "bulk approve" genuine.
- The `displayButton` filter means that if the selection ONLY contains
  already-approved rows, Approve disappears — selecting an already-
  `validate`/`refuse` distractor alongside the target is fine; the
  controller filters them out, leaving Approve enabled.

## `hr.leave` list view hides the description column by default

`hr_leave_view_tree` sets `<field name="name" optional="hidden"/>`. If
your oracle matches leave rows by description, click the optional-columns
dropdown (`.o_optional_columns_dropdown_toggle`) and tick the Description
entry first. Alternatively, match on the employee name — employee_id is
always visible.

## Default search facets on `/odoo/time-off-approval`

`hr_leave_action_action_approve_department` sets
`search_default_waiting_for_me=1`, `search_default_waiting_for_me_manager=2`,
`search_default_current_year=3`. To see all your seeded pending requests
regardless of employee-manager linkage, `clear_search_filters()` before
trying to tick rows. The "Waiting For Me" facet is scoped by
`leave_manager_id` — your seed must point every test employee's
`leave_manager_id` to admin if you rely on the default facets, or just
clear them all (oracle does the latter).

## action_refuse→action_draft cleanup order

To reset an already-validated leave for re-seed, call `action_refuse()`
then `action_draft()` — the sequence is what `test_leave_requests.py`
uses and what ships in the `request_time_off_approve` reference.
`action_draft()` alone raises on a `validate` record.

## State-diff spurious "create" from an extra hr.leave

Browser-use, when fumbling through the Time Off dashboard, sometimes
posts a hr.leave create with null `name` (description) — likely a misfire
on the "New Time Off" shortcut. This shows up as two extra diff rows
(`name=null, op=create` and `state=confirm, op=create`). If your state
spec tracks `hr.leave` by `name` match_key, these show as extras and
tank Precision even when the target leaves were approved correctly.
Either live with the F1 drop (the task still FAILs Strict) or move the
leave-creation detection fully into `check.py` and drop the generic
hr.leave track from `state_spec.yaml`.
