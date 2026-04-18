"""Seed for hr_attendance.kiosk_pin_check_in_then_manager_fix_checkout."""


EMPLOYEE_NAME = "Bench Kiosk Worker"


def setup(env):
    env["hr.attendance"].search([("employee_id.name", "=", EMPLOYEE_NAME)]).unlink()
    env["hr.employee"].search([("name", "=", EMPLOYEE_NAME)]).unlink()

    company = env.company
    company.write({
        "attendance_kiosk_mode": "manual",
        "attendance_kiosk_use_pin": True,
    })

    employee = env["hr.employee"].create({
        "name": EMPLOYEE_NAME,
        "company_id": company.id,
        "pin": "2468",
    })

    env["hr.attendance"].create({
        "employee_id": employee.id,
        "check_in": "2026-05-20 09:00:00",
        "check_out": False,
    })
