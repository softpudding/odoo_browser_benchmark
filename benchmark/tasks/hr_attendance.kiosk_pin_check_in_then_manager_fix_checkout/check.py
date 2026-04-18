"""Postcondition checks for hr_attendance.kiosk_pin_check_in_then_manager_fix_checkout."""


def check(env):
    failures = []

    employee = env["hr.employee"].search([("name", "=", "Bench Kiosk Worker")], limit=1)
    if not employee:
        return ["Employee 'Bench Kiosk Worker' not found"]

    attendances = env["hr.attendance"].search([
        ("employee_id", "=", employee.id),
        ("check_in", "=", "2026-05-20 09:00:00"),
    ])
    if len(attendances) != 1:
        return [f"Expected exactly 1 target attendance, found {len(attendances)}"]

    attendance = attendances[0]
    if str(attendance.check_out) != "2026-05-20 17:00:00":
        failures.append(
            f"Check out is {attendance.check_out}, expected 2026-05-20 17:00:00"
        )

    others = env["hr.attendance"].search([
        ("employee_id", "=", employee.id),
        ("id", "!=", attendance.id),
    ])
    if others:
        failures.append("Unexpected extra attendances were created for Bench Kiosk Worker")

    return failures
