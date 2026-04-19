"""Cleanup for hr.promote_employee_set_new_job_title_save."""

EMPLOYEE_NAME = "Bench Promote Me"


def cleanup(env):
    employees = env["hr.employee"].with_context(active_test=False).search(
        [("name", "=", EMPLOYEE_NAME)]
    )
    for emp in employees:
        emp.sudo().unlink()
