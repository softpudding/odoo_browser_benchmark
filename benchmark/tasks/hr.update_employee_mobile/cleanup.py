"""Clean up artifacts from previous runs."""

EMPLOYEE_NAME = "Amelia Stone"
DEPT_NAME = "Operations"


def cleanup(env):
    env["hr.employee"].search([("name", "=", EMPLOYEE_NAME)]).unlink()
    env["hr.department"].search([("name", "=", DEPT_NAME)]).unlink()
