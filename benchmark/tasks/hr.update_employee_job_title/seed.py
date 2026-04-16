"""Seed an employee for the job-title update task."""

EMPLOYEE_NAME = "Daniel Ortiz"
DEPT_NAME = "Support"
OLD_JOB_NAME = "Support Representative"
NEW_JOB_NAME = "Operations Specialist"


def setup(env):
    env["hr.employee"].search([("name", "=", EMPLOYEE_NAME)]).unlink()

    dept = env["hr.department"].search([("name", "=", DEPT_NAME)], limit=1)
    if not dept:
        dept = env["hr.department"].create({"name": DEPT_NAME})

    old_job = env["hr.job"].search([("name", "=", OLD_JOB_NAME)], limit=1)
    if not old_job:
        old_job = env["hr.job"].create({
            "name": OLD_JOB_NAME,
            "department_id": dept.id,
        })

    env["hr.job"].search([("name", "=", NEW_JOB_NAME)]).unlink()
    env["hr.job"].create({
        "name": NEW_JOB_NAME,
        "department_id": dept.id,
    })

    env["hr.employee"].create({
        "name": EMPLOYEE_NAME,
        "job_id": old_job.id,
        "department_id": dept.id,
        "work_email": "daniel.ortiz@example.com",
    })
