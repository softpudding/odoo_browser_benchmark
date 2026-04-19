# Cookbook notes - hr.create_public_holiday_calendar_entry

## Public Holidays menu + action — where it lives in Odoo 19

- Menu path: **Time Off → Configuration → Public Holidays**
  (menu_id `hr_holidays.hr_holidays_public_time_off_menu_configuration`,
  parent `menu_hr_holidays_configuration`, parent of that is
  `menu_hr_holidays_root` — the Time Off app root).
- Action: `hr_holidays.open_view_public_holiday`
  (addons/hr_holidays/views/resource_views.xml:83-98). The action is
  a filtered `list,form` view over `resource.calendar.leaves` with
  `domain=[('resource_id', '=', False)]` — i.e. **only company-wide
  entries**. Navigation URL that skips menu chrome:
  `/odoo/action-hr_holidays.open_view_public_holiday`.
- Access: only users with `hr_holidays.group_hr_holidays_manager`
  see the Configuration menu. Seed should ensure admin is in the
  manager group (base.user_admin usually is, belt-and-braces).

## `resource.calendar.leaves.calendar_id` default is EMPTY on this view

Contrary to what the task spec implied, on the Public Holidays list the
`calendar_id` cell shows placeholder **"All Schedules"** (blank) rather
than being pre-filled with the company's `resource_calendar_id`. The
field's compute (`_compute_calendar_id`) depends on `resource_id.calendar_id`,
and since the Public Holidays filter pins `resource_id=False`, the
compute produces no value. `company_id` is then computed from the
(empty) calendar_id and falls back to `self.env.company` via
`_compute_company_id`.

A public holiday with `calendar_id=False` is semantically valid —
it's a company-wide non-working period across every working
schedule. check.py should accept it; expected_state.json should
encode it as `"norm_value": null`.

## Daterange widget on an inline list — button → input transition

In the Public Holidays editable-bottom list, `date_from` and `date_to`
render via the `daterange` widget:

- Before click: each cell shows a `<button data-field="date_{from,to}">`
  with the current displayed value as `value` and `data-tooltip`.
- On clicking `button[data-field="date_from"]`: BOTH the start and end
  cells swap to `<input data-field="date_{from,to}">` and a floating
  `.o_datetime_picker` popover opens anchored on the clicked button.
- Subsequent clicks on `date_to` stay as `<input>` — the widget does
  NOT revert to button mode until focus leaves the row.

Oracle recipe for this transition:
1. `page.locator("button[data-field='date_from']").click()`
2. Wait for `input[data-field='date_from']`, type the datetime, Tab.
3. Type the end datetime into `input[data-field='date_to']`, Tab.
4. Close the picker by clicking a neutral area (NOT Escape — see below).
5. Click `button.o_list_button_save`.

## Escape DISCARDS an inline list row (loses all edits)

On `<list editable="bottom">` views, pressing Escape while a row is
selected unmounts the row and loses every pending edit. This is
**different** from form-view daterange usage where Escape simply closes
the picker.

Symptom: oracle types `name`, `date_from`, `date_to`, presses Escape to
dismiss the picker, then can't find the selected row — the row is gone
and the subsequent save_form() commits an empty list.

Fix: after Tab-ing out of the last cell, click a neutral target
outside the row (e.g. `.o_breadcrumb` at a small offset) to close the
floating picker without dispatching Escape to the list renderer.

## tz drift tolerance in check.py

The Odoo web datetime widget interprets typed strings in the browser's
local tz, not the admin user's Odoo tz. On a PDT host with admin.tz=UTC,
typing `06/01/2026 00:00:00` stores `2026-06-01 07:00:00 UTC` — whose
admin-local date (UTC) is 2026-06-01 at 07:00, but whose
`local_date_from.combine(date.min)` logic in other callers may pin it
to 2026-05-31. For a public-holiday-day task the right invariant is
"the stored span overlaps 2026-06-01 in ANY plausible tz". check.py
checks overlap against UTC, America/Los_Angeles, America/New_York,
Europe/Paris, Asia/Shanghai, Asia/Singapore and the admin tz, and
accepts if any one of them overlaps the target day. This is
defence-in-depth against harness tz surprises — same pattern as
`calendar.create_recurring_meeting_weekly_pattern`.

## state_spec `optional: true` kills diff-engine scoring

If the only tracked model in `state_spec.yaml` has `optional: true`,
`StateSnapshot.compute_edits()` skips it entirely (line 237 of
`benchmark/instrumentation/state_snapshot.py`: "if not include_optional
and spec.optional: continue"). Result: 0 atomic edits observed, 0
recall, F1=0.0 even when the record WAS correctly created. Drop the
`optional: true` line when you want the diff engine to score your
created record. The `optional: true` flag is reserved for models you
track solely for check.py / trace purposes (e.g. `calendar.event` in
the recurring-meeting task, which scores via check.py and keeps
`expected_state.json: []`).

## state_diff emits `op: create` for all new-record fields (incl. nulls)

Because the Bench Founder Day row did not exist in `before_state`,
every tracked field diffs as `op: "create"` — even ones with null
values (`resource_id=False`, `calendar_id=False`). expected_state.json
must list all four create entries (name, resource_id, calendar_id,
time_type) explicitly; omitting `calendar_id: null` and
`time_type: "leave"` yields "Unexpected extra edits" and drops
precision to 0.5. Using `op: "set"` for a newly-created record is
always wrong — the diff engine differentiates create vs set.

## Browser-use behaviour (calibration: BU PASS)

BU solved this single-shot in 120.8s, F1=1.0, 26 non-forbidden writes,
0 forbidden. The prompt's explicit menu trail (Time Off → Configuration
→ Public Holidays) plus the standard New-button + inline-row pattern
makes it straightforward for BU — no wizard, no radio dialog, no
cross-module round-trip. This is a **medium-tier** task primarily for
the daterange-on-inline-list widget trap; to push to tier-3, add a
non-default `calendar_id` requirement or a multi-row create with
duplicate-name deduplication.
