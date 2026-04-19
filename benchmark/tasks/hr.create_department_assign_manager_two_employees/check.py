"""Postcondition checks for hr.create_department_assign_manager_two_employees.

Validates:
1. Department 'Bench Ops' exists with manager_id = Bench Dept Manager.
2. Each of the two workers has department_id = Bench Ops.
3. Exactly 2 employees belong to the new department (no extras, no misses).
4. The manager has not been placed into the new department.
5. No employee was archived or deleted.
"""

NEW_DEPT_NAME = "Bench Ops"
MANAGER_NAME = "Bench Dept Manager"
WORKER_NAMES = ["Bench Dept Worker 1", "Bench Dept Worker 2"]


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

    # Each worker must be in the new department
    for name in WORKER_NAMES:
        emp = env["hr.employee"].with_context(active_test=False).search(
            [("name", "=", name)], limit=1
        )
        if not emp:
            failures.append(f"Worker '{name}' missing")
            continue
        if not emp.active:
            failures.append(f"Worker '{name}' was archived")
            continue
        if not emp.department_id:
            failures.append(f"Worker '{name}' has no department")
            continue
        if emp.department_id.name != NEW_DEPT_NAME:
            failures.append(
                f"Worker '{name}' department is "
                f"'{emp.department_id.name}', expected '{NEW_DEPT_NAME}'"
            )

    # Manager must still exist and should NOT have been placed into
    # the new department (the prompt explicitly says the manager stays
    # without a department).
    mgr = env["hr.employee"].with_context(active_test=False).search(
        [("name", "=", MANAGER_NAME)], limit=1
    )
    if not mgr:
        failures.append(f"Manager '{MANAGER_NAME}' missing")
    else:
        if not mgr.active:
            failures.append(f"Manager '{MANAGER_NAME}' was archived")
        if mgr.department_id and mgr.department_id.name == NEW_DEPT_NAME:
            failures.append(
                f"Manager '{MANAGER_NAME}' should NOT have been placed "
                f"into '{NEW_DEPT_NAME}'"
            )

    # Exactly 2 workers should be in the new department.
    # (Using the workers' explicit department_id above is already enough,
    # but we also assert the count so the agent cannot pad it with extras.)
    members_in_new_dept = env["hr.employee"].with_context(
        active_test=False
    ).search_count([("department_id", "=", dept.id)])
    # Allow exactly 2 (the two workers). If the manager happens to be
    # set as well, the previous manager-department check above will flag it.
    if members_in_new_dept != 2:
        failures.append(
            f"Department '{NEW_DEPT_NAME}' has {members_in_new_dept} "
            f"members, expected exactly 2"
        )

    return failures
