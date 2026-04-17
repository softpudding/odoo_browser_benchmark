"""Seed an employee for the work-email update task."""

EMPLOYEE_NAME = "Lena Ortiz"


def setup(env):
    existing = env["hr.employee"].search([("name", "=", EMPLOYEE_NAME)])
    existing.unlink()

    dept = env["hr.department"].search([("name", "=", "Operations")], limit=1)
    if not dept:
        dept = env["hr.department"].create({"name": "Operations"})

    job = env["hr.job"].search([("name", "=", "Operations Analyst")], limit=1)
    if not job:
        job = env["hr.job"].create({
            "name": "Operations Analyst",
            "department_id": dept.id,
        })

    env["hr.employee"].create({
        "name": EMPLOYEE_NAME,
        "job_id": job.id,
        "department_id": dept.id,
        "work_email": "lena.ortiz@acme.com",
        "work_phone": "+1 555 0330",
    })
