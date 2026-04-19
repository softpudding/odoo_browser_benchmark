"""Clean up artifacts from previous runs of
stock.receive_serial_tracked_product_two_serials."""

PICKING_NAME = "WH/IN/BENCH-SERIAL"
VENDOR_NAME = "Bench Serial Vendor"
PRODUCT_NAME = "Bench Serial Item"
EXPECTED_SERIALS = ("SN-BENCH-A001", "SN-BENCH-A002")


def cleanup(env):
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
            quants = env["stock.quant"].search(
                [("product_id", "in", prods.ids)]
            )
            for q in quants:
                try:
                    q.with_context(inventory_mode=True).write(
                        {"inventory_quantity": 0.0}
                    )
                    q.action_apply_inventory()
                except Exception:
                    pass
            try:
                quants.unlink()
            except Exception:
                pass
        except Exception:
            pass
        try:
            env["stock.lot"].search(
                [("product_id", "in", prods.ids)]
            ).unlink()
        except Exception:
            pass
        try:
            prods.mapped("product_tmpl_id").unlink()
        except Exception:
            pass

    stale_lots = env["stock.lot"].search(
        [("name", "in", list(EXPECTED_SERIALS))]
    )
    if stale_lots:
        try:
            stale_lots.unlink()
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
