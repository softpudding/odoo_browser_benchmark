"""Cleanup for hr_attendance.kiosk_pin_check_in_then_manager_fix_checkout."""


def cleanup(env):
    env["hr.attendance"].search([("employee_id.name", "=", "Bench Kiosk Worker")]).unlink()
    env["hr.employee"].search([("name", "=", "Bench Kiosk Worker")]).unlink()
