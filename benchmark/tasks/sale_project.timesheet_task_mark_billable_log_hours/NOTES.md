# sale_project.timesheet_task_mark_billable_log_hours — ABORTED (missing dependency)

## Status: NOT IMPLEMENTED

This task was aborted during creation because the required Odoo modules for
timesheet-driven billing are **not installed** in the benchmark snapshot.

## Module check (as of 2026-04-18 against `benchmark_validate`)

| Module          | State       |
|-----------------|-------------|
| `project`       | installed   |
| `sale_project`  | installed   |
| `hr_timesheet`  | uninstalled |
| `sale_timesheet`| uninstalled |

Both `hr_timesheet` and `sale_timesheet` are required for the intended workflow:

- `hr_timesheet` adds the Timesheets tab to `project.task` and the
  `account.analytic.line` timesheet records.
- `sale_timesheet` bridges timesheet `unit_amount` to
  `sale.order.line.qty_delivered` when the service product is configured with
  `service_policy='delivered_timesheet'`.

Without these modules:

1. There is no Timesheets tab on the task form — the agent has no UI to log
   hours.
2. `product.template.service_policy` selection does not include
   `delivered_timesheet` (that value is contributed by `sale_timesheet`), so
   the seed's service product cannot even be configured correctly.
3. `qty_delivered` cannot be computed from timesheets, breaking the core
   validation step.

## Resolution path

Per the task creation instructions, the worktree is forbidden from installing
modules. This task should be revisited once the benchmark snapshot is
regenerated with `sale_timesheet` (which pulls in `hr_timesheet` as a
dependency) installed.

## What was NOT created

- `prompt.md`
- `seed.py`
- `task.yaml`
- `state_spec.yaml` / `trace_spec.yaml`
- `expected_state.json`
- `check.py`
- `cleanup.py`
- `oracle.py`

Only this `NOTES.md` is committed so the row in `STATUS.md` has a tangible
artifact documenting the abort reason.
