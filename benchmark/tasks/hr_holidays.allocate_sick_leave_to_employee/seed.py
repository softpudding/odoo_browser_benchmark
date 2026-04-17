"""Seed for hr_holidays.allocate_sick_leave_to_employee.

Ensure a "Benchmark Allocatee" employee and user exist, and that a
"Sick Time Off" leave type is available with requires_allocation=True.
Clean up any stale allocations before the task runs.
"""


EMPLOYEE_NAME = "Benchmark Allocatee"
USER_LOGIN = "benchmark_allocatee"
LEAVE_TYPE = "Sick Time Off"


def _unlink_allocations(env, employee):
    allocs = env["hr.leave.allocation"].with_context(active_test=False).search([
        ("employee_id", "=", employee.id),
    ])
    for alloc in allocs:
        if alloc.state in ("validate", "validate1"):
            try:
                alloc.action_refuse()
            except Exception:
                pass
    allocs.with_context(allocation_skip_state_check=True).unlink()


def setup(env):
    user = env["res.users"].with_context(active_test=False).search(
        [("login", "=", USER_LOGIN)], limit=1
    )
    employee = None
    if user:
        employee = env["hr.employee"].with_context(active_test=False).search(
            [("user_id", "=", user.id)], limit=1
        )

    if not employee:
        employee = env["hr.employee"].with_context(active_test=False).search(
            [("name", "=", EMPLOYEE_NAME)], limit=1
        )

    if employee:
        _unlink_allocations(env, employee)
        leaves = env["hr.leave"].with_context(active_test=False).search([
            ("employee_id", "=", employee.id),
        ])
        for lv in leaves:
            if lv.state == "validate":
                try:
                    lv.action_refuse()
                    lv.action_draft()
                except Exception:
                    pass
            elif lv.state in ("confirm", "validate1"):
                try:
                    lv.action_draft()
                except Exception:
                    pass
        leaves.unlink()
        employee.with_context(allocation_skip_state_check=True).unlink()

    if user:
        user.unlink()

    # Ensure leave type exists
    leave_type = env["hr.leave.type"].with_context(active_test=False).search(
        [("name", "=", LEAVE_TYPE)], limit=1
    )
    if not leave_type:
        leave_type = env["hr.leave.type"].create({
            "name": LEAVE_TYPE,
            "requires_allocation": True,
            "leave_validation_type": "hr",
            "allocation_validation_type": "hr",
            "employee_requests": False,
        })
    else:
        leave_type.write({
            "requires_allocation": True,
            "allocation_validation_type": "hr",
        })

    # Create fresh user + employee
    user = env["res.users"].create({
        "name": EMPLOYEE_NAME,
        "login": USER_LOGIN,
        "email": "benchmark.allocatee@example.com",
    })
    env["hr.employee"].create({
        "name": EMPLOYEE_NAME,
        "user_id": user.id,
        "work_email": "benchmark.allocatee@example.com",
    })
