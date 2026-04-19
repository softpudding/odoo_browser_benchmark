"""Postcondition checks for hr.generate_employee_card_set_badge_id."""


EMPLOYEE_NAME = "Bench Worker Badge"
EXPECTED_BADGE = "EMPBENCH001"


def check(env):
    failures = []

    employee = env["hr.employee"].search([("name", "=", EMPLOYEE_NAME)], limit=1)
    if not employee:
        return [f"Employee '{EMPLOYEE_NAME}' not found"]

    if employee.barcode != EXPECTED_BADGE:
        failures.append(
            f"Badge ID (barcode) is {employee.barcode!r}, expected {EXPECTED_BADGE!r}"
        )

    # Guard: no rogue archival / rename
    if not employee.active:
        failures.append(f"Employee '{EMPLOYEE_NAME}' was archived")
    if employee.name != EMPLOYEE_NAME:
        failures.append(f"Employee name changed to {employee.name!r}")

    return failures
