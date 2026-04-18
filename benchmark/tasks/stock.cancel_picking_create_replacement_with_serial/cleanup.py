"""Clean up artifacts from previous runs of
stock.cancel_picking_create_replacement_with_serial."""

ORIGINAL_ORIGIN = "R-BENCH-CANCEL-001"
VENDOR_NAME = "Bench Supplier Inc"
WRONG_PRODUCT_NAME = "Bench Hardware Item"
SERIAL_PRODUCT_NAME = "Bench Serial Widget"


def cleanup(env):
    pickings = env["stock.picking"].search([
        "|",
        ("origin", "=", ORIGINAL_ORIGIN),
        ("partner_id.name", "=", VENDOR_NAME),
    ])
    for pick in pickings:
        if pick.state not in ("done", "cancel"):
            try:
                pick.action_cancel()
            except Exception:
                pass
        try:
            pick.move_ids.write({"state": "cancel"})
            pick.write({"state": "cancel"})
            pick.unlink()
        except Exception:
            pass

    for pname in (WRONG_PRODUCT_NAME, SERIAL_PRODUCT_NAME):
        prods = env["product.product"].search([("name", "=", pname)])
        env["stock.move.line"].search([("product_id", "in", prods.ids)]).unlink()
        env["stock.move"].search([("product_id", "in", prods.ids)]).unlink()
        env["stock.lot"].search([("product_id", "in", prods.ids)]).unlink()
        try:
            prods.mapped("product_tmpl_id").unlink()
        except Exception:
            pass

    stale_lots = env["stock.lot"].search([("name", "in", ["BS-001", "BS-002"])])
    if stale_lots:
        try:
            stale_lots.unlink()
        except Exception:
            pass

    vendor = env["res.partner"].search([("name", "=", VENDOR_NAME)], limit=1)
    if vendor:
        # Only remove if nothing else references it.
        other = env["stock.picking"].search([("partner_id", "=", vendor.id)])
        if not other:
            try:
                vendor.unlink()
            except Exception:
                pass
