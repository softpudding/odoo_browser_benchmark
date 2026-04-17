"""Cleanup for hr_holidays.refuse_leave_request."""


def cleanup(env):
    leaves = env["hr.leave"].with_context(active_test=False).search([
        ("name", "=", "Unscheduled absence — please refuse"),
    ])
    for l in leaves:
        if l.state in ("validate", "confirm", "validate1", "refuse"):
            try:
                l.action_draft()
            except Exception:
                pass
    leaves.unlink()
