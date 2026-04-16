"""Clean up artifacts from previous runs."""

EMPLOYEE_NAME = "Sofia Chen"


def cleanup(env):
    emp = env["hr.employee"].search([("name", "=", EMPLOYEE_NAME)])
    emp.unlink()
