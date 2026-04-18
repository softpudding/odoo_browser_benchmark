"""Cleanup for hr_attendance.clock_in_out_kiosk_mode."""

EMPLOYEE_NAME = "Bench Worker"


def cleanup(env):
    env["hr.attendance"].sudo().search(
        [("employee_id.name", "=", EMPLOYEE_NAME)]
    ).unlink()
    employees = env["hr.employee"].with_context(active_test=False).search(
        [("name", "=", EMPLOYEE_NAME)]
    )
    for emp in employees:
        emp.sudo().unlink()
