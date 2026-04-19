"""Cleanup artifacts from previous runs of stock.cancel_picking_abandoned."""

PICKING_NAME = "WH/OUT/BENCH-CANCEL"
CUSTOMER_NAME = "Bench Cancel Ship Co"
PRODUCT_NAME = "Bench Cancel Prod"


def cleanup(env):
    pickings = env["stock.picking"].with_context(active_test=False).search([
        "|",
        ("name", "=", PICKING_NAME),
        "&",
        ("partner_id.name", "=", CUSTOMER_NAME),
        ("picking_type_id.code", "=", "outgoing"),
    ])
    ordered = sorted(pickings, key=lambda p: 0 if p.backorder_id else 1)
    for pick in ordered:
        if pick.state not in ("done", "cancel"):
            try:
                pick.action_cancel()
            except Exception:
                pass
        try:
            pick.move_ids.write({"state": "cancel"})
        except Exception:
            pass
        try:
            pick.write({"state": "cancel"})
        except Exception:
            pass
        try:
            pick.unlink()
        except Exception:
            pass

    prods = env["product.product"].with_context(active_test=False).search(
        [("name", "=", PRODUCT_NAME)]
    )
    if prods:
        try:
            env["stock.move.line"].search(
                [("product_id", "in", prods.ids)]
            ).unlink()
        except Exception:
            pass
        try:
            env["stock.move"].search(
                [("product_id", "in", prods.ids)]
            ).unlink()
        except Exception:
            pass
        try:
            env["stock.quant"].with_context(inventory_mode=True).search(
                [("product_id", "in", prods.ids)]
            ).unlink()
        except Exception:
            pass
        try:
            prods.mapped("product_tmpl_id").unlink()
        except Exception:
            pass

    customer = env["res.partner"].with_context(active_test=False).search(
        [("name", "=", CUSTOMER_NAME)], limit=1
    )
    if customer:
        other = env["stock.picking"].search([("partner_id", "=", customer.id)])
        if not other:
            try:
                customer.unlink()
            except Exception:
                pass
