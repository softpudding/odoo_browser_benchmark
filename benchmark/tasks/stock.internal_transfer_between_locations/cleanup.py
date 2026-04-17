"""Cleanup for stock.internal_transfer_between_locations."""

PRODUCT_NAME = "Benchmark Shelf Widget"
ORIGIN = "BENCH-INT-SHELF-A1"
SUBLOC_NAME = "Shelf A1"


def cleanup(env):
    pickings = env["stock.picking"].search([("origin", "=", ORIGIN)])
    for p in pickings:
        if p.state not in ("done", "cancel"):
            try:
                p.action_cancel()
            except Exception:
                pass
    pickings.filtered(lambda p: p.state != "done").unlink()
    # Product and sub-location stay — they are cheap and harmless for future runs.
