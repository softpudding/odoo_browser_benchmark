"""Clean up artifacts from previous runs of stock.transfer_lot_tracked_product."""

PRODUCT_NAME = "Lot Product A"
RECEIPT_ORIGIN = "BENCH-TRANSFER-LOT-01"
LOT_NAME = "LOT-2026-001"


def cleanup(env):
    for pick in env["stock.picking"].search([("origin", "=", RECEIPT_ORIGIN)]):
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
    if prods:
        env["stock.move.line"].search([("product_id", "in", prods.ids)]).unlink()
        env["stock.move"].search([("product_id", "in", prods.ids)]).unlink()
        env["stock.quant"].search([("product_id", "in", prods.ids)]).unlink()
        env["stock.lot"].search([("product_id", "in", prods.ids)]).unlink()
        prods.mapped("product_tmpl_id").unlink()

    env["stock.lot"].search([("name", "=", LOT_NAME)]).unlink()
