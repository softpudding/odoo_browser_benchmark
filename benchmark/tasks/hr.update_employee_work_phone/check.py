"""Postcondition checks for hr.update_employee_work_phone."""


def check(env):
    failures = []

    employee = env["hr.employee"].search([("name", "=", "Sofia Chen")], limit=1)
    if not employee:
        return ["Employee 'Sofia Chen' not found"]

    if employee.work_phone != "+1 555 0211":
        failures.append(
            f"Work Phone is {employee.work_phone!r}, expected '+1 555 0211'"
        )

    if employee.work_email != "sofia.chen@example.com":
        failures.append(
            f"Work Email changed to {employee.work_email!r}, expected 'sofia.chen@example.com'"
        )

    return failures
