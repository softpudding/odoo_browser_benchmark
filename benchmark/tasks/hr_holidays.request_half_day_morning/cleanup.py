"""Clean up requests created during the task."""


def cleanup(env):
    leaves = env["hr.leave"].with_context(active_test=False).search([
        ("name", "=", "Doctor appointment"),
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
