"""Cleanup for hr_holidays.cancel_approved_leave_and_reallocate."""


def cleanup(env):
    leaves = env["hr.leave"].with_context(active_test=False).search([
        ("name", "in", [
            "Family vacation (tentative)",
            "Family vacation (confirmed)",
        ]),
    ])
    for leave in leaves:
        if leave.state == "validate":
            try:
                leave.action_refuse()
            except Exception:
                pass
        if leave.state in ("confirm", "validate1", "refuse"):
            try:
                leave.action_draft()
            except Exception:
                pass
    leaves.unlink()
