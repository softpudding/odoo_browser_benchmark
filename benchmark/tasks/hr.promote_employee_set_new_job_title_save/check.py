"""Postcondition checks for hr.promote_employee_set_new_job_title_save."""


EMPLOYEE_NAME = "Bench Promote Me"
OLD_JOB_TITLE = "Analyst"
NEW_JOB_TITLE = "Senior Analyst"
WORK_EMAIL = "bench.promote@example.com"


def check(env):
    failures = []

    employees = env["hr.employee"].with_context(active_test=False).search(
        [("name", "=", EMPLOYEE_NAME)]
    )

    if len(employees) == 0:
        return [
            f"Employee '{EMPLOYEE_NAME}' not found — it must not be "
            "renamed, deleted, or archived."
        ]
    if len(employees) > 1:
        return [
            f"Expected exactly 1 hr.employee named '{EMPLOYEE_NAME}'; "
            f"found {len(employees)} (duplicate?)."
        ]

    employee = employees[0]

    if not employee.active:
        failures.append(
            f"Employee '{EMPLOYEE_NAME}' must remain active (not archived)."
        )

    if employee.job_title != NEW_JOB_TITLE:
        failures.append(
            f"Job Title is {employee.job_title!r}, expected "
            f"{NEW_JOB_TITLE!r}."
        )

    # Guard: the agent must not change unrelated fields.
    if employee.name != EMPLOYEE_NAME:
        failures.append(
            f"Employee name changed to {employee.name!r}; expected "
            f"{EMPLOYEE_NAME!r}."
        )

    if (employee.work_email or "") != WORK_EMAIL:
        failures.append(
            f"work_email changed to {employee.work_email!r}; expected "
            f"{WORK_EMAIL!r}."
        )

    # Must not accidentally set a Job Position (job_id m2o).
    if employee.job_id:
        failures.append(
            f"Job Position (job_id) should be empty but was set to "
            f"{employee.job_id.display_name!r} — the task only asks to "
            "edit the Job Title char field."
        )

    return failures
