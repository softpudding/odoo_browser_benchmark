"""Clean up artifacts from previous runs."""


REFS = ["GLOBEX-OLD", "GLOBEX-NEW", "GLOBEX-PLC", "GLOBEX-LABS"]


def cleanup(env):
    Partner = env["res.partner"].with_context(active_test=False)
    stale = Partner.search([("ref", "in", REFS)])
    for p in stale:
        p.active = True
    stale.unlink()
