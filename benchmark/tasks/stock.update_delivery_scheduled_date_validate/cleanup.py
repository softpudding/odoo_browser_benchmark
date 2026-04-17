"""Clean up artifacts from previous runs."""


def cleanup(env):
    pickings = env["stock.picking"].search([("origin", "in", ["BENCH-DEL-DATE-01", "BENCH-DEL-DATE-OTHER"])])
    for pk in pickings:
        if pk.state not in ("cancel", "done"):
            pk.action_cancel()
        pk.unlink()
