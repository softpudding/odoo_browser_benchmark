"""Postcondition checks for hr.update_employee_job_title."""

EMPLOYEE_NAME = "Daniel Ortiz"
TARGET_JOB = "Operations Specialist"
OLD_JOB = "Support Representative"


def check(env):
    failures = []

    employee = env["hr.employee"].search([("name", "=", EMPLOYEE_NAME)], limit=1)
    if not employee:
        return [f"Employee '{EMPLOYEE_NAME}' not found"]

    if not employee.job_id:
        failures.append("Job Position not set")
    elif employee.job_id.name != TARGET_JOB:
        failures.append(f"Job Position is '{employee.job_id.name}', expected '{TARGET_JOB}'")

    if employee.job_id and employee.job_id.name == OLD_JOB:
        pass

    if (employee.work_email or "") != "daniel.ortiz@example.com":
        failures.append(
            f"Work email changed to '{employee.work_email}', expected 'daniel.ortiz@example.com'"
        )

    return failures
