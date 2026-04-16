"""Cleanup for hr.add_employee_skill."""

EMPLOYEE_NAME = "Priya Mehta"


def cleanup(env):
    employees = env["hr.employee"].search([("name", "=", EMPLOYEE_NAME)])
    for emp in employees:
        emp.employee_skill_ids.unlink()
        emp.unlink()
