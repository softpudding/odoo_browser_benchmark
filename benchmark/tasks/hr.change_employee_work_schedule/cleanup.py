"""Cleanup for hr.change_employee_work_schedule.

Removes the seeded 'Bench Sched Me' employee. We leave the
'Part Time 20h' resource.calendar in place — seed re-ensures it on
each run, and leaving it idempotently does not affect other tasks.
"""


EMPLOYEE_NAME = "Bench Sched Me"


def cleanup(env):
    employees = env["hr.employee"].with_context(active_test=False).search(
        [("name", "=", EMPLOYEE_NAME)]
    )
    for emp in employees:
        emp.sudo().unlink()
