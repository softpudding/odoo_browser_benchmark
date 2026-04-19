"""Cleanup for hr_timesheet.log_time_for_2_days_approve_via_manager.

BLOCKED TASK — required modules are not available in this checkout.
Cleanup is a no-op to avoid NameError on missing models.
"""


def cleanup(env):
    sheet_mod = env["ir.module.module"].search(
        [("name", "=", "hr_timesheet_sheet")], limit=1
    )
    ts_mod = env["ir.module.module"].search(
        [("name", "=", "hr_timesheet")], limit=1
    )
    if (
        not sheet_mod
        or sheet_mod.state != "installed"
        or not ts_mod
        or ts_mod.state != "installed"
    ):
        return
    # Once the modules are installed, cleanup should remove:
    #  - the seeded hr.employee 'Bench Dev' and its res.users
    #  - the seeded project.project 'Bench Approve Proj' and its task
    #  - any account.analytic.line / timesheet.sheet leftovers
