"""Cleanup for hr_holidays.approve_multiple_requests_bulk.

Removes the four bench leaves, then the four bench employees and their
user accounts so subsequent seed runs can re-create them cleanly.
"""


LEAVE_NAMES = [
    "Bench Alice vacation",
    "Bench Bob vacation",
    "Bench Carol vacation",
    "Bench Diana vacation",
]

EMPLOYEE_LOGINS = [
    "bench_alice",
    "bench_bob",
    "bench_carol",
    "bench_diana",
]


def cleanup(env):
    # Drop bench leaves first (they reference the employees).
    leaves = env["hr.leave"].with_context(active_test=False).search([
        ("name", "in", LEAVE_NAMES),
    ])
    for l in leaves:
        try:
            if l.state == "validate":
                l.action_refuse()
                l.action_draft()
            elif l.state in ("confirm", "validate1", "refuse"):
                l.action_draft()
        except Exception:
            pass
    try:
        leaves.unlink()
    except Exception:
        pass

    # Drop the bench employees, then their users.
    users = env["res.users"].with_context(active_test=False).search([
        ("login", "in", EMPLOYEE_LOGINS),
    ])
    employees = env["hr.employee"].with_context(active_test=False).search([
        ("user_id", "in", users.ids),
    ])
    try:
        employees.unlink()
    except Exception:
        pass
    try:
        users.unlink()
    except Exception:
        pass
