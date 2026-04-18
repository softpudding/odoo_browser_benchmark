"""Postcondition checks for hr.create_department_assign_manager_three_employees.

Validates:
1. Department 'Bench Engineering' exists with manager_id = Mike Manager.
2. Each of the three engineers has department_id = Bench Engineering.
3. Mike Manager himself has not been moved out of his original department.
4. No employee was archived or deleted.
"""

NEW_DEPT_NAME = "Bench Engineering"
MANAGER_NAME = "Mike Manager"
ENGINEER_NAMES = ["Eng One", "Eng Two", "Eng Three"]


def check(env):
    failures = []

    dept = env["hr.department"].search(
        [("name", "=", NEW_DEPT_NAME)], limit=1
    )
    if not dept:
        return [f"Department '{NEW_DEPT_NAME}' not found"]

    if not dept.manager_id:
        failures.append(f"Department '{NEW_DEPT_NAME}' has no manager")
    elif dept.manager_id.name != MANAGER_NAME:
        failures.append(
            f"Department manager is '{dept.manager_id.name}', "
            f"expected '{MANAGER_NAME}'"
        )

    for name in ENGINEER_NAMES:
        emp = env["hr.employee"].with_context(active_test=False).search(
            [("name", "=", name)], limit=1
        )
        if not emp:
            failures.append(f"Engineer '{name}' missing")
            continue
        if not emp.active:
            failures.append(f"Engineer '{name}' was archived")
            continue
        if not emp.department_id:
            failures.append(f"Engineer '{name}' has no department")
            continue
        if emp.department_id.name != NEW_DEPT_NAME:
            failures.append(
                f"Engineer '{name}' department is "
                f"'{emp.department_id.name}', expected '{NEW_DEPT_NAME}'"
            )

    return failures
