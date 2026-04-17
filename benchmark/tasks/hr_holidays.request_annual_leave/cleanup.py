"""Clean up artifacts from previous runs."""


def cleanup(env):
    leaves = env["hr.leave"].with_context(active_test=False).search([
        ("name", "=", "Family vacation to Iceland"),
    ])
    for leave in leaves:
        if leave.state == "validate":
            leave.action_refuse()
            leave.action_draft()
        elif leave.state in ("confirm", "validate1"):
            leave.action_draft()
    leaves.unlink()
