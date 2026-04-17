"""Seed an employee for the mobile-number update task."""

EMPLOYEE_NAME = "Amelia Stone"
DEPT_NAME = "Operations"


def setup(env):
    env["hr.employee"].search([("name", "=", EMPLOYEE_NAME)]).unlink()
    env["hr.department"].search([("name", "=", DEPT_NAME)]).unlink()

    department = env["hr.department"].create({
        "name": DEPT_NAME,
    })

    env["hr.employee"].create({
        "name": EMPLOYEE_NAME,
        "department_id": department.id,
        "mobile_phone": "+1 555 0150",
        "work_email": "amelia.stone@example.com",
    })
