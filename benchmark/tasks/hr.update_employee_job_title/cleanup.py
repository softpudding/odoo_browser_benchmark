"""Clean up artifacts from previous runs."""

EMPLOYEE_NAME = "Daniel Ortiz"


def cleanup(env):
    emp = env["hr.employee"].search([("name", "=", EMPLOYEE_NAME)], limit=1)
    if emp:
        emp.unlink()

    for job_name in ("Support Representative", "Operations Specialist"):
        env["hr.job"].search([("name", "=", job_name)]).unlink()

    env["hr.department"].search([("name", "=", "Support")]).unlink()
