"""Cleanup for hr.add_skill_to_employee_with_level."""

EMPLOYEE_NAME = "Tech Tom"


def cleanup(env):
    employees = env["hr.employee"].with_context(active_test=False).search(
        [("name", "=", EMPLOYEE_NAME)]
    )
    for emp in employees:
        emp.employee_skill_ids.unlink()
        emp.sudo().unlink()
