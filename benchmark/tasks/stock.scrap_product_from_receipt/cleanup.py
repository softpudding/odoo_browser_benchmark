"""Clean up stock.scrap_product_from_receipt artifacts."""


def cleanup(env):
    ref = "BENCH-SCRAP-REC-01"
    env["stock.scrap"].search([("origin", "=", ref)]).unlink()
    picks = env["stock.picking"].search([("origin", "=", ref)])
    for pick in picks:
        if pick.state not in ("cancel", "done"):
            pick.action_cancel()
        pick.unlink()

