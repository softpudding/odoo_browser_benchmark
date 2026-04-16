"""Postcondition checks for hr.update_work_information.

Validates:
1. Employee "Sofia Chen" exists
2. Work location is "Home"
3. Timezone is "America/New_York"
4. Certificate level is "master"
5. Job and department unchanged
"""

EMPLOYEE_NAME = "Sofia Chen"


def check(env):
    failures = []

    emp = env["hr.employee"].search([("name", "=", EMPLOYEE_NAME)], limit=1)
    if not emp:
        return [f"Employee '{EMPLOYEE_NAME}' not found"]

    # Check work location
    if not emp.work_location_id:
        failures.append("Work location not set")
    elif emp.work_location_id.name != "Home":
        failures.append(
            f"Work location is '{emp.work_location_id.name}', expected 'Home'"
        )

    # Check timezone
    if emp.tz != "America/New_York":
        failures.append(
            f"Timezone is '{emp.tz}', expected 'America/New_York'"
        )

    # Check certificate
    if emp.certificate != "master":
        failures.append(
            f"Certificate is '{emp.certificate}', expected 'master'"
        )

    # Check unchanged fields
    if emp.job_id and emp.job_id.name != "Software Developer":
        failures.append(
            f"Job changed to '{emp.job_id.name}', expected 'Software Developer'"
        )
    if emp.department_id and emp.department_id.name != "Engineering":
        failures.append(
            f"Department changed to '{emp.department_id.name}', expected 'Engineering'"
        )

    return failures
