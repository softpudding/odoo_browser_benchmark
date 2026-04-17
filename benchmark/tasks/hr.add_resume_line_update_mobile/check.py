"""Postcondition checks for hr.add_resume_line_update_mobile."""

from datetime import date


EMPLOYEE_NAME = "Marina Ortega"
RESUME_TITLE = "ISO 27001 Internal Auditor"


def check(env):
    failures = []

    employee = env["hr.employee"].search([("name", "=", EMPLOYEE_NAME)], limit=1)
    if not employee:
        return [f"Employee '{EMPLOYEE_NAME}' not found"]

    if employee.work_location_id.name != "Home":
        failures.append(
            f"Work location is '{employee.work_location_id.name}', expected 'Home'"
        )

    lines = employee.resume_line_ids.filtered(lambda line: line.name == RESUME_TITLE)
    if len(lines) != 1:
        failures.append(
            f"Expected 1 matching resume line, found {len(lines)}"
        )
    else:
        line = lines[0]
        if line.line_type_id.name != "Certification":
            failures.append(
                f"Resume line section is '{line.line_type_id.name}', expected 'Certification'"
            )
        if line.date_start != date(2026, 5, 1):
            failures.append(
                f"Resume line start date is {line.date_start}, expected 2026-05-01"
            )
        if line.date_end != date(2027, 5, 1):
            failures.append(
                f"Resume line end date is {line.date_end}, expected 2027-05-01"
            )

    if len(employee.resume_line_ids) != 1:
        failures.append(
            f"Expected exactly 1 resume entry, found {len(employee.resume_line_ids)}"
        )

    return failures
