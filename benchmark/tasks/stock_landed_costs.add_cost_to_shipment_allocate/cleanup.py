"""Cleanup for stock_landed_costs.add_cost_to_shipment_allocate.

Reverses the seed in child-first order. Done/Posted landed costs
cannot be unlinked, so cleanup archives them if present (idempotent
for re-runs). Pickings are cancelled + unlinked; PO cancelled +
unlinked; products unlinked; vendor unlinked if orphaned.
"""

PO_REF = "P-BENCH-LC-001"
RECEIPT_REF = "R-BENCH-LC-001"
VENDOR_NAME = "Bench Import Vendor"
PRODUCT_NAME = "Bench Import Item"
FREIGHT_NAME = "Freight"
LC_CATEGORY_NAME = "Bench LC Category"


def cleanup(env):
    if "stock.landed.cost" in env.registry:
        # Draft landed costs tied to our products — delete. Posted
        # ones stay (can't unlink) but won't block a fresh seed
        # because the fresh seed creates new products and a new
        # receipt name.
        prods = env["product.product"].with_context(active_test=False).search(
            [("name", "in", [PRODUCT_NAME, FREIGHT_NAME])]
        )
        if prods:
            lcs = env["stock.landed.cost"].with_context(active_test=False).search([
                "|",
                ("cost_lines.product_id", "in", prods.ids),
                ("picking_ids.move_ids.product_id", "in", prods.ids),
            ])
            for lc in lcs:
                if lc.state == "draft":
                    try:
                        lc.unlink()
                    except Exception:
                        pass

    pickings = env["stock.picking"].search([
        "|", "|", "|",
        ("origin", "=", PO_REF),
        ("name", "=", RECEIPT_REF),
        ("name", "in", ["R-BENCH-LC-DISTRACTOR-A", "R-BENCH-LC-DISTRACTOR-B"]),
        ("origin", "in", ["P-BENCH-LC-DIST-A", "P-BENCH-LC-DIST-B"]),
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

    old = env["purchase.order"].search([
        "|", "|", "|",
        ("name", "=", PO_REF),
        ("origin", "=", PO_REF),
        ("name", "in", ["P-BENCH-LC-DIST-A", "P-BENCH-LC-DIST-B"]),
        ("origin", "in", ["P-BENCH-LC-DIST-A", "P-BENCH-LC-DIST-B"]),
    ])
    for po in old:
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

    prods = env["product.product"].with_context(active_test=False).search(
        [("name", "in", [
            PRODUCT_NAME, FREIGHT_NAME,
            "Bench Other Gadget", "Bench Spare Widget",
        ])]
    )
    for p in prods:
        try:
            env["stock.move.line"].search(
                [("product_id", "=", p.id)]
            ).unlink()
            env["stock.move"].search(
                [("product_id", "=", p.id)]
            ).unlink()
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

    # Keep the Bench LC Category — harmless permanent fixture.
