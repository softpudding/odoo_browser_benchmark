# Cookbook notes — hr.promote_employee_set_new_job_title_save

## Odoo 19 quirk / sanity checks

- `hr.employee` has TWO fields that look alike in the form but are
  distinct:
  * `job_id` — many2one on `hr.job` (label "Job Position").
  * `job_title` — `Char` (label "Job Title"), rendered directly below
    Job Position on the default "Work" tab
    (`addons/hr/views/hr_employee_views.xml:161`).
  The existing task `hr.update_employee_job_title` actually edits
  `job_id` (its name is misleading). This new task intentionally
  targets the `job_title` char field as an "easy anchor" single-char
  edit, distinct from row 425 (barcode / badge) and row 341 (skills).
- Seeding `job_title='Analyst'` on a freshly created employee with no
  `job_id` keeps the diff engine's view clean: a single
  `set job_title='Senior Analyst'` atomic edit.
- Because the Job Title field is on the default tab, the oracle
  doesn't need `click_tab`; `fill_field(page, "job_title", ...)`
  works directly after `click_list_row` + `_wait_for_ready`.

## Browser-use behavior

- BU (single shot, 89.8s): opened Employees, opened `Bench Promote Me`,
  replaced `Analyst` with `Senior Analyst` in the Job Title field, and
  saved. F1=1.0, 0 postcondition failures, strict clean trace. Easy
  anchor calibration confirmed — no wizard, no tab switching, single
  char field edit.
