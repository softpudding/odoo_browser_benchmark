"""Clean up artifacts from previous runs."""


def cleanup(env):
    for origin in ("BENCH-DEL-01", "BENCH-DEL-OTHER"):
        old_pickings = env["stock.picking"].search([("origin", "=", origin)])
        for pk in old_pickings:
            if pk.state not in ("cancel", "done"):
                pk.action_cancel()
            pk.unlink()
