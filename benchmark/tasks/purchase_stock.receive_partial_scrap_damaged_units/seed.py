"""Seed for purchase_stock.receive_partial_scrap_damaged_units.

Category: deep_ui_interaction (HARD).

Seeds:
  * Vendor 'Bench Reliable Supplier' (supplier_rank=1).
  * Storable product 'Bench Widget' (list_price 5.0, purchase_ok=True).
  * Scrap reason tag 'Damaged' (selected in the scrap wizard).
  * A confirmed purchase.order with origin 'BENCH-SCRAP-RCV-01' holding
    one line: 10 x Bench Widget at 5.00/unit. The confirmation creates
    the incoming stock.picking the agent must receive.

The agent must:
  1. Open the PO / receipt.
  2. Scrap 2 units of Bench Widget via the Scrap action menu with the
     'Damaged' reason tag.
  3. Set the receipt Done quantity on the Bench Widget move line to 8.
  4. Validate the receipt and pick 'No Backorder' in the wizard.
"""

VENDOR_NAME = "Bench Reliable Supplier"
PRODUCT_NAME = "Bench Widget"
PO_ORIGIN = "BENCH-SCRAP-RCV-01"
REASON_TAG = "Damaged"


def setup(env):
    Partner = env["res.partner"]
    Product = env["product.product"]
    Template = env["product.template"]
    PO = env["purchase.order"]
    POL = env["purchase.order.line"]
    Scrap = env["stock.scrap"]
    ReasonTag = env["stock.scrap.reason.tag"]

    # --- Cleanup prior runs -------------------------------------------------
    # Remove stale scraps for Bench Widget (draft ones only — done scraps
    # can't be unlinked without force, but they won't interfere because we
    # also drop the product template below).
    old_scraps = Scrap.with_context(active_test=False).search([
        ("product_id.name", "=", PRODUCT_NAME),
    ])
    for s in old_scraps:
        if s.state == "draft":
            try:
                s.unlink()
            except Exception:
                pass

    # Cancel + delete any prior PO with this origin.
    vendor = Partner.search([("name", "=", VENDOR_NAME)], limit=1)
    if vendor:
        old_pos = PO.search([
            ("partner_id", "=", vendor.id),
            ("origin", "=", PO_ORIGIN),
        ])
        for po in old_pos:
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

    # Clean up leftover pickings by origin if vendor was not found yet.
    old_picks = env["stock.picking"].search([
        ("origin", "=", PO_ORIGIN),
        ("state", "!=", "done"),
    ])
    for p in old_picks:
        try:
            p.action_cancel()
        except Exception:
            pass
        try:
            p.unlink()
        except Exception:
            pass

    # Drop leftover product templates to keep the database clean.
    stale_prods = Product.search([("name", "=", PRODUCT_NAME)])
    stale_tmpl = stale_prods.mapped("product_tmpl_id")
    try:
        stale_tmpl.unlink()
    except Exception:
        pass

    # --- Vendor -------------------------------------------------------------
    vendor = Partner.search([("name", "=", VENDOR_NAME)], limit=1)
    if not vendor:
        vendor = Partner.create({
            "name": VENDOR_NAME,
            "email": "orders@bench-reliable.example.com",
            "supplier_rank": 1,
        })
    else:
        vendor.write({"supplier_rank": 1})

    # --- Scrap reason tag ---------------------------------------------------
    tag = ReasonTag.search([("name", "=", REASON_TAG)], limit=1)
    if not tag:
        tag = ReasonTag.create({"name": REASON_TAG})

    # --- Product ------------------------------------------------------------
    tmpl = Template.create({
        "name": PRODUCT_NAME,
        "type": "consu",
        "is_storable": True,
        "list_price": 5.0,
        "standard_price": 5.0,
        "purchase_ok": True,
        "sale_ok": True,
    })
    product = tmpl.product_variant_id

    # --- Create + confirm PO (this generates the incoming picking) ---------
    # Use PO_ORIGIN as the PO name as well, so the generated incoming
    # picking's `origin` field is a deterministic, human-readable value
    # (Odoo copies PO.name into picking.origin).
    po = PO.create({
        "name": PO_ORIGIN,
        "partner_id": vendor.id,
        "origin": PO_ORIGIN,
    })
    POL.create({
        "order_id": po.id,
        "product_id": product.id,
        "product_qty": 10.0,
        "price_unit": 5.0,
        "name": PRODUCT_NAME,
    })
    po.button_confirm()

    # Reserve / assign incoming picking so move lines are populated.
    picking = po.picking_ids[:1]
    if picking:
        try:
            picking.action_assign()
        except Exception:
            pass

    assert po.state == "purchase", (
        f"Seed failed: PO state is '{po.state}', expected 'purchase'"
    )
    assert picking, "Seed failed: no incoming picking was created by button_confirm"
    assert picking.state not in ("done", "cancel"), (
        f"Seed failed: picking state is '{picking.state}', expected a draft/assigned receipt"
    )
