"""Clean up artifacts from previous runs."""

RECEIPT_REF = "BENCH-RCV-01"


def cleanup(env):
    picks = env["stock.picking"].search([("origin", "=", RECEIPT_REF)])
    for pick in picks:
        try:
            if pick.state != "done":
                pick.action_cancel()
            pick.unlink()
        except Exception:
            pass
