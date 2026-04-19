"""Postcondition checks for hr_timesheet.log_time_for_2_days_approve_via_manager.

BLOCKED TASK — hr_timesheet_sheet (Enterprise-only) is not available in
this checkout and hr_timesheet is not in base_modules.txt, so the task
cannot run end-to-end. The check below returns a clear failure so the
eval pipeline flags it rather than appearing as a spurious PASS.
"""


def check(env):
    sheet_mod = env["ir.module.module"].search(
        [("name", "=", "hr_timesheet_sheet")], limit=1
    )
    ts_mod = env["ir.module.module"].search(
        [("name", "=", "hr_timesheet")], limit=1
    )

    if not sheet_mod or sheet_mod.state == "uninstallable":
        return [
            "BLOCKED: hr_timesheet_sheet (Enterprise-only) is uninstallable "
            "in this Odoo Community checkout — submit/approve lifecycle on "
            "timesheets cannot be validated end-to-end."
        ]
    if not ts_mod or ts_mod.state != "installed":
        return [
            "BLOCKED: hr_timesheet is not installed in benchmark_base. "
            "Add it to benchmark/base_modules.txt before unblocking."
        ]

    # Concrete validation to add once the modules are available:
    #  - exactly two account.analytic.line rows for employee 'Bench Dev' on
    #    project 'Bench Approve Proj' / task 'Development', with
    #    unit_amount=8.0 and date 2026-04-15 / 2026-04-16
    #  - both lines reference the same timesheet.sheet record
    #  - sheet.state == 'done' (approved by admin/manager)
    #  - chatter on the sheet shows submit + approve transitions
    return [
        "BLOCKED: modules were available but check body not yet "
        "implemented. See STATUS.md row 429 for context."
    ]
