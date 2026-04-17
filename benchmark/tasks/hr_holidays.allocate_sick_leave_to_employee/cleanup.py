"""Clean up allocations created during the task."""


def cleanup(env):
    allocs = env["hr.leave.allocation"].with_context(active_test=False).search([
        ("name", "=", "2026 Sick leave pool"),
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
