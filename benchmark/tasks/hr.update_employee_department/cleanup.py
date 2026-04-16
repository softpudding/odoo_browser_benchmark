"""Clean up artifacts from previous runs."""

EMPLOYEE_NAME = "Sofia Chen"


def cleanup(env):
    env["hr.employee"].search([("name", "=", EMPLOYEE_NAME)]).unlink()