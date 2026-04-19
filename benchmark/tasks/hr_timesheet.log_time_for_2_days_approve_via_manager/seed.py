"""Seed for hr_timesheet.log_time_for_2_days_approve_via_manager.

BLOCKED TASK — the submit/approve timesheet workflow requires the
Enterprise-only `hr_timesheet_sheet` (a.k.a. `timesheet.sheet`) addon,
whose source is not present in this Odoo 19 Community checkout.

Additionally, `hr_timesheet` itself is not listed in
`benchmark/base_modules.txt`, so it is not installed in the
`benchmark_base` snapshot used for the benchmark.

This seed raises a clear error so the eval pipeline records the blocker
instead of silently crashing inside the browser phase.
"""


def setup(env):
    sheet_mod = env["ir.module.module"].search(
        [("name", "=", "hr_timesheet_sheet")], limit=1
    )
    ts_mod = env["ir.module.module"].search(
        [("name", "=", "hr_timesheet")], limit=1
    )

    if not sheet_mod or sheet_mod.state == "uninstallable":
        raise RuntimeError(
            "BLOCKED: hr_timesheet_sheet (Enterprise-only) is not available "
            "in this Odoo 19 Community checkout. The submit-to-manager / "
            "approve lifecycle on timesheets requires this addon. "
            "See STATUS.md row 429 for details."
        )
    if not ts_mod or ts_mod.state != "installed":
        raise RuntimeError(
            "BLOCKED: hr_timesheet is not installed in benchmark_base. "
            "Add `hr_timesheet` to benchmark/base_modules.txt and rebuild "
            "the snapshot before unblocking this task. "
            "See STATUS.md row 429 for details."
        )

    # Concrete seed body to add when the above modules are available:
    #  1. Ensure admin employee exists and is a timesheet manager.
    #  2. Create hr.employee 'Bench Dev' + its internal user with groups
    #     hr_timesheet.group_hr_timesheet_user + hr.group_hr_user, parent
    #     employee = admin.employee_id so admin is the manager.
    #  3. Create project.project 'Bench Approve Proj' with allow_timesheets
    #     and a task 'Development'.
    #  4. Leave the sheet + analytic lines un-seeded; the agent must create
    #     them through the UI.
    raise NotImplementedError(
        "Seed body intentionally left empty — flesh out when "
        "hr_timesheet_sheet (Enterprise) is available and "
        "hr_timesheet is installed in the base snapshot."
    )
