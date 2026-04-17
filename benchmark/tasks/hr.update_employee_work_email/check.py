"""Postcondition checks for hr.update_employee_work_email."""

EMPLOYEE_NAME = "Lena Ortiz"


def check(env):
    failures = []

    employee = env["hr.employee"].search([("name", "=", EMPLOYEE_NAME)], limit=1)
    if not employee:
        return [f"Employee '{EMPLOYEE_NAME}' not found"]

    if (employee.work_email or "") != "lena.ortiz@ops.example.com":
        failures.append(
            f"Work Email is '{employee.work_email}', expected 'lena.ortiz@ops.example.com'"
        )

    if (employee.work_phone or "") != "+1 555 0330":
        failures.append(
            f"Work Phone changed to '{employee.work_phone}', expected '+1 555 0330'"
        )

    return failures
