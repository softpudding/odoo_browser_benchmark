"""Clean up artifacts from previous runs of stock.receive_lot_tracked_product."""

PRODUCT_NAME = "Apex Turbine Rotor"
RECEIPT_ORIGIN = "BENCH-LOT-RCV-01"


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
    env["stock.move.line"].search([("product_id", "in", prods.ids)]).unlink()
    env["stock.move"].search([("product_id", "in", prods.ids)]).unlink()
    env["stock.lot"].search([("product_id", "in", prods.ids)]).unlink()
    prods.mapped("product_tmpl_id").unlink()
