"""Cleanup for hr.generate_employee_card_set_badge_id."""

EMPLOYEE_NAME = "Bench Worker Badge"


def cleanup(env):
    employees = env["hr.employee"].with_context(active_test=False).search(
        [("name", "=", EMPLOYEE_NAME)]
    )
    for emp in employees:
        emp.sudo().unlink()
