# Log 2 days of timesheets, submit to manager, approve (BLOCKED)

> **Note**: This task is BLOCKED in the Odoo 19 Community Edition checkout
> used for this benchmark. The required submit-to-manager / validate
> workflow on timesheet records is provided by the Enterprise-only
> `hr_timesheet_sheet` (a.k.a. `timesheet.sheet`) addon, whose source is
> not vendored in `addons/`. The Community `hr_timesheet` addon has no
> `state`, `validated`, or `sheet_id` fields on `account.analytic.line`,
> so there is no approval lifecycle to exercise through the UI.
>
> In addition, `hr_timesheet` is not listed in `benchmark/base_modules.txt`,
> so it is not installed in the `benchmark_base` snapshot: the
> `/odoo/timesheets` menu and the Timesheets tab on `project.task` do not
> appear in the stock benchmark DB.
>
> The original task intent is preserved below for future re-scoping when
> the `hr_timesheet_sheet` Enterprise addon (or an equivalent submit /
> approve mechanism) is available and `hr_timesheet` is added to
> `base_modules.txt`.

You will complete a multi-day timesheet approval workflow involving two
roles (employee + manager).

A seeded project `Bench Approve Proj`, task `Development`, and employee
`Bench Dev` (internal user with the hr timesheet user + officer groups)
already exist.

## Phase 1 — Employee: log time on 2 different dates

1. Switch to the `Bench Dev` user.
2. Open `/odoo/timesheets`.
3. Create a timesheet entry on `2026-04-15` for project `Bench Approve Proj`,
   task `Development`, 8 hours (`unit_amount=8.0`).
4. Create a second timesheet entry on `2026-04-16` with the same project/
   task and 8 hours.

## Phase 2 — Employee: submit the weekly sheet for approval

5. Open the containing timesheet sheet (week of 2026-04-13 → 2026-04-19).
6. Click **Submit to Manager**. The sheet transitions `draft → confirm`.

## Phase 3 — Manager: approve the submitted sheet

7. Switch to the `admin` user (who is `Bench Dev`'s manager).
8. Open the pending sheet under `Timesheets → To Approve`.
9. Click **Approve**. The sheet transitions `confirm → done`.

## Rules

- The two `account.analytic.line` rows must have `unit_amount=8.0`
  (resp. date=2026-04-15 and date=2026-04-16).
- Both rows must be attached to the submitted sheet, and the sheet's
  `state` must be `done` when the agent finishes.
- The entries must be for the seeded `Bench Dev` employee on project
  `Bench Approve Proj` / task `Development`.
