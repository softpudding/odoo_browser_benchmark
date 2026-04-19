# Cookbook notes — hr.change_employee_work_schedule

## Odoo 19 quirks / sanity checks

- `hr.employee.resource_calendar_id` is a Many2one to
  `resource.calendar`. Its **UI label is "Working Hours"** (see
  `addons/hr/models/hr_version.py:139` — `string="Working Hours"`).
  It is NOT called "Working Schedule" or "Work Schedule" in the form
  even though many modules reference a "schedule" concept.
- The field is rendered on the employee form under the **Payroll tab
  > Schedule section**
  (`addons/hr/views/hr_employee_views.xml:353`), guarded by
  `groups="hr.group_hr_manager"`. Admin has access. The field is
  NOT on the default "Work" tab, so the oracle must `click_tab(
  page, "Payroll")` before calling `set_many2one`.
- The company default schedule seeded by the `resource` module is
  `resource.resource_calendar_std` — name
  `"Standard 40 hours/week"` — with
  `full_time_required_hours=40`. It is the default for new
  `hr.employee` records unless overridden.
- `resource.calendar.hours_per_week` is a *stored compute* depending
  on `attendance_ids.hour_from/hour_to`, but is `readonly=False` and
  can be written directly. For this easy task we write both
  `hours_per_week=20` and `full_time_required_hours=20` explicitly on
  the seeded `Part Time 20h` calendar without touching
  `attendance_ids` — the spec only requires these two numeric
  invariants, and leaving `attendance_ids=[]` is valid.

## Differentiation vs adjacent rows

- Row 476 (hr.update_employee_job_title): Char field edit (`job_title`).
- Row 425 (hr.generate_employee_card_set_badge_id): Badge/barcode Char.
- Row 494 (this task): Single many2one change on
  `resource_calendar_id` with a Payroll-tab detour, easy anchor.
  The only UI wrinkle is the tab switch; the m2o itself is a
  standard autocomplete.

## Browser-use behavior

- BU (single shot, 70.8s, steps=0): navigated Employees, opened
  `Bench Sched Me`, switched to Payroll, changed Working Hours to
  `Part Time 20h` via autocomplete, saved. F1=1.0, 0 postcondition
  failures, strict clean trace, 16 non-forbidden writes. Easy
  calibration confirmed — the Payroll-tab detour did not trip BU.

## Seed idempotency

- `_cleanup` deletes any prior `Bench Sched Me` before seeding.
- `_ensure_part_time_calendar` searches with `active_test=False` and
  re-activates + re-writes hour fields if the calendar existed from a
  prior run. `cleanup.py` deliberately leaves `Part Time 20h` in
  place between runs (idempotent) since seed re-ensures its
  invariants.
