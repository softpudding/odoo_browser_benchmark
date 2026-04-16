"""Seed an employee for the update-department task.

Category: deep_ui_interaction (EASY).
Starting state: Employee "Sofia Chen" with department "Sales".
The agent must change the department to "Engineering".
"""

EMPLOYEE_NAME = "Sofia Chen"


def setup(env):
    env["hr.employee"].search([("name", "=", EMPLOYEE_NAME)]).unlink()

    dept_sales = env["hr.department"].search([("name", "=", "Sales")], limit=1)
    if not dept_sales:
        dept_sales = env["hr.department"].create({"name": "Sales"})

    dept_eng = env["hr.department"].search([("name", "=", "Engineering")], limit=1)
    if not dept_eng:
        dept_eng = env["hr.department"].create({"name": "Engineering"})

    job = env["hr.job"].search([("name", "=", "Sales Representative")], limit=1)
    if not job:
        job = env["hr.job"].create({
            "name": "Sales Representative",
            "department_id": dept_sales.id,
        })

    env["hr.employee"].create({
        "name": EMPLOYEE_NAME,
        "job_id": job.id,
        "department_id": dept_sales.id,
        "work_email": "sofia.chen@company.com",
        "work_phone": "+1 555 0200",
    })