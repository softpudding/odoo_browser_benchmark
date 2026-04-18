"""Cleanup for product_expiry.receive_lot_set_expiry_date."""

PRODUCT_NAME = "Bench Perishable"
RECEIPT_ORIGIN = "BENCH-PERISH-RCV-01"
LOT_NAME = "BP-LOT-001"


def cleanup(env):
    for pick in env["stock.picking"].search(
        [("origin", "=", RECEIPT_ORIGIN)]
    ):
        if pick.state not in ("done", "cancel"):
            try:
                pick.action_cancel()
            except Exception:
                pass
        try:
            pick.unlink()
        except Exception:
            pass

    prods = env["product.product"].search([("name", "=", PRODUCT_NAME)])
    env["stock.move.line"].search(
        [("product_id", "in", prods.ids)]
    ).unlink()
    env["stock.move"].search(
        [("product_id", "in", prods.ids)]
    ).unlink()
    env["stock.lot"].search(
        [("product_id", "in", prods.ids)]
    ).unlink()
    try:
        prods.mapped("product_tmpl_id").unlink()
    except Exception:
        pass

    stale = env["stock.lot"].search([("name", "=", LOT_NAME)])
    if stale:
        try:
            stale.unlink()
        except Exception:
            pass
