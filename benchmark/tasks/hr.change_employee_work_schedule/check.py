"""Postcondition checks for hr.change_employee_work_schedule."""


EMPLOYEE_NAME = "Bench Sched Me"
WORK_EMAIL = "bench.sched@example.com"
JOB_TITLE = "Operations"
PART_TIME_CALENDAR_NAME = "Part Time 20h"


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

    # Primary assertion: Working Hours m2o points at 'Part Time 20h'.
    target = env["resource.calendar"].search(
        [("name", "=", PART_TIME_CALENDAR_NAME)], limit=1
    )
    if not target:
        failures.append(
            f"Target resource.calendar '{PART_TIME_CALENDAR_NAME}' does "
            "not exist — seed should have created it."
        )
    else:
        if employee.resource_calendar_id.id != target.id:
            failures.append(
                f"Working Hours (resource_calendar_id) is "
                f"{employee.resource_calendar_id.display_name!r} "
                f"(id={employee.resource_calendar_id.id}); expected "
                f"{PART_TIME_CALENDAR_NAME!r} (id={target.id})."
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

    if (employee.job_title or "") != JOB_TITLE:
        failures.append(
            f"job_title changed to {employee.job_title!r}; expected "
            f"{JOB_TITLE!r}."
        )

    # Must not accidentally set a Job Position (job_id m2o).
    if employee.job_id:
        failures.append(
            f"Job Position (job_id) should be empty but was set to "
            f"{employee.job_id.display_name!r} — the task only asks to "
            "change the Working Hours field."
        )

    # Guard: ensure the target calendar wasn't renamed/tampered with.
    if target:
        if target.name != PART_TIME_CALENDAR_NAME:
            failures.append(
                f"Target resource.calendar name is {target.name!r}; "
                f"expected {PART_TIME_CALENDAR_NAME!r}."
            )

    return failures
