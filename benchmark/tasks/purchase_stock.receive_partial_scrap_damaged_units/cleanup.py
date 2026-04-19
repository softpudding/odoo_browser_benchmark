"""Cleanup for purchase_stock.receive_partial_scrap_damaged_units."""

VENDOR_NAME = "Bench Reliable Supplier"
PRODUCT_NAME = "Bench Widget"
PO_ORIGIN = "BENCH-SCRAP-RCV-01"


def cleanup(env):
    Partner = env["res.partner"]
    PO = env["purchase.order"]
    Product = env["product.product"]
    Scrap = env["stock.scrap"]

    # Delete any draft scraps on Bench Widget (done scraps can't be unlinked).
    stale = Scrap.with_context(active_test=False).search([
        ("product_id.name", "=", PRODUCT_NAME),
    ])
    for s in stale:
        if s.state == "draft":
            try:
                s.unlink()
            except Exception:
                pass

    vendor = Partner.search([("name", "=", VENDOR_NAME)], limit=1)
    if vendor:
        pos = PO.search([
            ("partner_id", "=", vendor.id),
            ("origin", "=", PO_ORIGIN),
        ])
        for po in pos:
            for pick in po.picking_ids:
                if pick.state not in ("done", "cancel"):
                    try:
                        pick.action_cancel()
                    except Exception:
                        pass
                if pick.state != "done":
                    try:
                        pick.unlink()
                    except Exception:
                        pass
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

    # Dangling pickings by origin.
    leftover_picks = env["stock.picking"].search([("origin", "=", PO_ORIGIN)])
    for p in leftover_picks:
        if p.state not in ("done", "cancel"):
            try:
                p.action_cancel()
            except Exception:
                pass
            try:
                p.unlink()
            except Exception:
                pass

    prods = Product.search([("name", "=", PRODUCT_NAME)])
    try:
        prods.mapped("product_tmpl_id").unlink()
    except Exception:
        pass

    # Leave the 'Damaged' reason tag in place — done scraps may reference it.
