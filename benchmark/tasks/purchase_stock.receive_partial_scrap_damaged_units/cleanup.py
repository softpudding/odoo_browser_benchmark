"""Clean up artifacts from previous runs of
purchase_stock.receive_partial_scrap_damaged_units."""

PO_ORIGIN = "P-BENCH-DMG-001"
VENDOR_NAME = "Bench Parts Vendor"
PRODUCT_NAME = "Bench Parts"
LOST_LOCATION_NAME = "Lost"


def cleanup(env):
    # Stock scraps for our product — unlink drafts, leave done (can't
    # delete). They will still reference archived records but won't
    # interfere with a re-seed.
    prods = env["product.product"].search([("name", "=", PRODUCT_NAME)])
    if prods:
        scraps = env["stock.scrap"].with_context(active_test=False).search([
            ("product_id", "in", prods.ids),
        ])
        for s in scraps:
            if s.state == "draft":
                try:
                    s.unlink()
                except Exception:
                    pass

    pickings = env["stock.picking"].search([
        "|",
        ("origin", "=", PO_ORIGIN),
        "&",
        ("partner_id.name", "=", VENDOR_NAME),
        ("picking_type_id.code", "=", "incoming"),
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

    old_pos = env["purchase.order"].search([
        "|",
        ("name", "=", PO_ORIGIN),
        ("origin", "=", PO_ORIGIN),
    ])
    for po in old_pos:
        if po.state in ("purchase", "done"):
            try:
                po.button_cancel()
            except Exception:
                pass
        if po.state == "cancel":
            try:
                po.button_draft()
            except Exception:
                pass
        try:
            po.unlink()
        except Exception:
            pass

    for p in prods:
        try:
            env["stock.move.line"].search([("product_id", "=", p.id)]).unlink()
            env["stock.move"].search([("product_id", "=", p.id)]).unlink()
        except Exception:
            pass
    try:
        prods.mapped("product_tmpl_id").unlink()
    except Exception:
        pass

    vendor = env["res.partner"].search([("name", "=", VENDOR_NAME)], limit=1)
    if vendor:
        other = env["stock.picking"].search([("partner_id", "=", vendor.id)])
        other_po = env["purchase.order"].search([("partner_id", "=", vendor.id)])
        if not other and not other_po:
            try:
                vendor.unlink()
            except Exception:
                pass

    # Keep the WH/Lost location around — it's a useful permanent fixture.
