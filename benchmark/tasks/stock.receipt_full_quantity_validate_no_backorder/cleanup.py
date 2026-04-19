"""Cleanup artifacts from stock.receipt_full_quantity_validate_no_backorder."""

PICKING_NAME = "WH/IN/BENCH-FULL"
VENDOR_NAME = "Bench Vendor"
PRODUCT_NAME = "Bench Recv Item"


def cleanup(env):
    # Pickings (original + any backorders or duplicates).
    pickings = env["stock.picking"].search([
        "|",
        ("name", "=", PICKING_NAME),
        "&",
        ("partner_id.name", "=", VENDOR_NAME),
        ("picking_type_id.code", "=", "incoming"),
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

    vendor = env["res.partner"].search(
        [("name", "=", VENDOR_NAME)], limit=1
    )
    if vendor:
        other_pickings = env["stock.picking"].search(
            [("partner_id", "=", vendor.id)]
        )
        if not other_pickings:
            try:
                vendor.unlink()
            except Exception:
                pass
