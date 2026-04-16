"""Postcondition checks for hr.update_employee_department.

Validates:
1. Employee "Sofia Chen" exists
2. Department is "Engineering"
3. Job position unchanged
"""

EMPLOYEE_NAME = "Sofia Chen"


def check(env):
    failures = []

    emp = env["hr.employee"].search([("name", "=", EMPLOYEE_NAME)], limit=1)
    if not emp:
        return [f"Employee '{EMPLOYEE_NAME}' not found"]

    if not emp.department_id:
        failures.append("Department not set")
    elif emp.department_id.name != "Engineering":
        failures.append(f"Department is '{emp.department_id.name}', expected 'Engineering'")

    if emp.job_id and emp.job_id.name != "Sales Representative":
        failures.append(f"Job changed to '{emp.job_id.name}', expected 'Sales Representative'")

    return failures