"""Oracle for hr_timesheet.log_time_for_2_days_approve_via_manager.

BLOCKED TASK — the `hr_timesheet_sheet` (Enterprise-only) addon is not
present in this Odoo 19 Community checkout, and `hr_timesheet` is not
installed in `benchmark_base`. The oracle exits with a clear error so
the harness records the blocker instead of producing spurious results.

To flesh out once the modules are available:
  1. Switch to Bench Dev, open /odoo/timesheets.
  2. Create 2 analytic lines (2026-04-15 8h, 2026-04-16 8h) on
     Bench Approve Proj / Development.
  3. Submit the week's timesheet sheet to manager.
  4. Switch to admin (manager) and approve the sheet; verify state=done.
"""

from benchmark.oracle_helpers import run_oracle


def oracle(page):
    raise RuntimeError(
        "BLOCKED: hr_timesheet_sheet is Enterprise-only and absent from "
        "this Odoo Community checkout; hr_timesheet is not in "
        "base_modules.txt. Oracle body intentionally short-circuits. "
        "See STATUS.md row 429."
    )


run_oracle(oracle)
