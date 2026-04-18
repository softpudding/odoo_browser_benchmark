"""Cleanup for hr_holidays.bulk_approve_two_pending_requests."""


LEAVE_NAMES = [
    "Family vacation",
    "Wedding attendance",
    "Personal errands",
    "Already approved holiday",
    "Already refused day",
]


def cleanup(env):
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
    leaves.unlink()
