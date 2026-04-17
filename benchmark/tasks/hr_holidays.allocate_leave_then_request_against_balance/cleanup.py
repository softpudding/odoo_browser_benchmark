"""Clean up records created during hr_holidays.allocate_leave_then_request_against_balance."""


def cleanup(env):
    leaves = env["hr.leave"].with_context(active_test=False).search([
        ("name", "=", "Warehouse flu recovery"),
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

    allocs = env["hr.leave.allocation"].with_context(active_test=False).search([
        ("name", "=", "Quarter-End Sick Leave Buffer"),
    ])
    for alloc in allocs:
        if alloc.state == "validate":
            try:
                alloc.action_refuse()
            except Exception:
                pass
        if alloc.state in ("confirm", "validate1", "refuse"):
            try:
                alloc.action_draft()
            except Exception:
                pass
    allocs.unlink()
