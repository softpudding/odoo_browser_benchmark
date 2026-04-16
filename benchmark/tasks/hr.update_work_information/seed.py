"""Seed an employee for the update-work-information task.

Category 2 (MEDIUM): Navigate across two tabs (Work Information and
Private Information) on an employee form and update fields. Browser-use
may miss the second tab or fail to save changes across multiple tabs.
"""

EMPLOYEE_NAME = "Sofia Chen"


def setup(env):
    # --- Cleanup prior runs ---
    old_emp = env["hr.employee"].search([("name", "=", EMPLOYEE_NAME)])
    old_emp.unlink()

    # --- Ensure work location "Home" exists ---
    home_loc = env["hr.work.location"].search(
        [("name", "=", "Home")], limit=1
    )
    if not home_loc:
        home_loc = env["hr.work.location"].create({
            "name": "Home",
        })

    # --- Find or create department ---
    dept = env["hr.department"].search(
        [("name", "=", "Engineering")], limit=1
    )
    if not dept:
        dept = env["hr.department"].create({"name": "Engineering"})

    # --- Find or create job ---
    job = env["hr.job"].search(
        [("name", "=", "Software Developer")], limit=1
    )
    if not job:
        job = env["hr.job"].create({
            "name": "Software Developer",
            "department_id": dept.id,
        })

    # --- Create employee ---
    env["hr.employee"].create({
        "name": EMPLOYEE_NAME,
        "job_id": job.id,
        "department_id": dept.id,
        "work_email": "sofia.chen@company.com",
        "work_phone": "+1 555 0200",
        "tz": "America/Los_Angeles",
        "certificate": "bachelor",
    })
