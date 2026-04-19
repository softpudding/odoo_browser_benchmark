"""Cleanup for hr_holidays.request_sick_leave_approve_self."""


EMPLOYEE_LOGIN = "bench_sick_employee"


def cleanup(env):
    user = env["res.users"].search([("login", "=", EMPLOYEE_LOGIN)], limit=1)
    if not user:
        return
    employee = env["hr.employee"].search([("user_id", "=", user.id)], limit=1)
    if not employee:
        return

    leaves = env["hr.leave"].with_context(active_test=False).search([
        ("employee_id", "=", employee.id),
    ])
    for leave in leaves:
        try:
            if leave.state == "validate":
                leave.action_refuse()
        except Exception:
            pass
        try:
            if leave.state in ("confirm", "validate1", "refuse"):
                leave.action_draft()
        except Exception:
            pass
    leaves.unlink()
