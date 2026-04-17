"""Postcondition checks for hr.update_employee_mobile."""

EMPLOYEE_NAME = "Amelia Stone"
TARGET_MOBILE = "+1 555 0472"
EXPECTED_EMAIL = "amelia.stone@example.com"


def check(env):
    failures = []

    employee = env["hr.employee"].search([("name", "=", EMPLOYEE_NAME)], limit=1)
    if not employee:
        return [f"Employee '{EMPLOYEE_NAME}' not found"]

    if (employee.mobile_phone or "").strip() != TARGET_MOBILE:
        failures.append(
            f"Mobile is '{employee.mobile_phone}', expected '{TARGET_MOBILE}'"
        )

    if (employee.work_email or "").strip() != EXPECTED_EMAIL:
        failures.append(
            f"Work email is '{employee.work_email}', expected '{EXPECTED_EMAIL}'"
        )

    return failures
