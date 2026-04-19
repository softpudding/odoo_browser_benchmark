"""Cleanup artifacts from stock.delivery_transfer_validate_partial_backorder_no."""

PICKING_NAME = "WH/OUT/BENCH-BACKORDER-NO"
CUSTOMER_NAME = "Bench Ship Co"
PRODUCT_NAME = "Bench Pick Item"


def cleanup(env):
    # Pickings (original + any backorders or duplicates).
    pickings = env["stock.picking"].search([
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

    prods = env["product.product"].search([("name", "=", PRODUCT_NAME)])
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

    customer = env["res.partner"].search(
        [("name", "=", CUSTOMER_NAME)], limit=1
    )
    if customer:
        other_pickings = env["stock.picking"].search(
            [("partner_id", "=", customer.id)]
        )
        if not other_pickings:
            try:
                customer.unlink()
            except Exception:
                pass
