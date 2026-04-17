"""Clean up artifacts from previous runs."""


EMPLOYEE_NAME = "Benchmark Allocatee"
USER_LOGIN = "benchmark_allocatee"


def cleanup(env):
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
