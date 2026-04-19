"""Cleanup for hr_holidays.request_allocation_approve_self_book_day_off."""


ALLOC_DESC = "Q2 bonus"
LEAVE_DESC = "Bench day off"


def cleanup(env):
    leaves = env["hr.leave"].with_context(active_test=False).search([
        ("name", "=", LEAVE_DESC),
    ])
    for l in leaves:
        try:
            if l.state == "validate":
                l.action_refuse()
        except Exception:
            pass
        try:
            if l.state in ("confirm", "validate1", "refuse"):
                l.action_draft()
        except Exception:
            pass
    leaves.unlink()

    allocs = env["hr.leave.allocation"].with_context(active_test=False).search([
        ("name", "=", ALLOC_DESC),
    ])
    for a in allocs:
        try:
            if a.state == "validate":
                a.action_refuse()
        except Exception:
            pass
        try:
            if a.state in ("confirm", "validate1", "refuse"):
                a.action_draft()
        except Exception:
            pass
    allocs.unlink()
