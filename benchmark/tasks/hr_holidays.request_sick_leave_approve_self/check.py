"""Postcondition checks for hr_holidays.request_sick_leave_approve_self."""

from datetime import date


LEAVE_TYPE_NAME = "Sick Leave"
EMPLOYEE_NAME = "Bench Sick Employee"
EXPECTED_DATE_FROM = date(2026, 5, 11)
EXPECTED_DATE_TO = date(2026, 5, 12)


def check(env):
    failures = []

    employee = env["hr.employee"].search(
        [("name", "=", EMPLOYEE_NAME)], limit=1
    )
    if not employee:
        failures.append(f"Employee '{EMPLOYEE_NAME}' is missing")
        return failures

    leave_type = env["hr.leave.type"].search(
        [("name", "=", LEAVE_TYPE_NAME)], limit=1
    )
    if not leave_type:
        failures.append(f"Leave type '{LEAVE_TYPE_NAME}' is missing")
        return failures

    leaves = env["hr.leave"].with_context(active_test=False).search([
        ("employee_id", "=", employee.id),
        ("holiday_status_id", "=", leave_type.id),
    ])
    if not leaves:
        failures.append(
            f"No hr.leave found for {EMPLOYEE_NAME} / {LEAVE_TYPE_NAME}"
        )
        return failures
    if len(leaves) > 1:
        failures.append(
            f"Found {len(leaves)} Sick Leave records for {EMPLOYEE_NAME}, "
            f"expected exactly 1"
        )

    leave = leaves[0]

    if leave.state != "validate":
        failures.append(
            f"Leave state is '{leave.state}', expected 'validate' "
            f"(must be approved end-to-end)"
        )

    if leave.request_date_from != EXPECTED_DATE_FROM:
        failures.append(
            f"Leave start date is {leave.request_date_from}, "
            f"expected {EXPECTED_DATE_FROM}"
        )
    if leave.request_date_to != EXPECTED_DATE_TO:
        failures.append(
            f"Leave end date is {leave.request_date_to}, "
            f"expected {EXPECTED_DATE_TO}"
        )

    # Ensure holiday_status_id and employee_id really match the expected values
    # (defensive — the search filter already does this, but state_diff may not
    # have the match_key).
    if leave.holiday_status_id.name != LEAVE_TYPE_NAME:
        failures.append(
            f"Leave type is '{leave.holiday_status_id.name}', "
            f"expected '{LEAVE_TYPE_NAME}'"
        )
    if leave.employee_id.name != EMPLOYEE_NAME:
        failures.append(
            f"Leave employee is '{leave.employee_id.name}', "
            f"expected '{EMPLOYEE_NAME}'"
        )

    return failures
