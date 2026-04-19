"""Seed for purchase.create_rfq_receive_invoice_3way_match (HARD).

Category: closed_loop_cross_module.
Full 3-way match: the agent creates the RFQ from scratch, confirms it,
partially receives in the Inventory-ish receipt form with a backorder,
then returns to the PO and creates + posts the vendor bill.

This task combines three proven hard patterns:
  * create-from-scratch with exact field values (phantom empty lines)
  * inline Done-qty edit in the receipt (A: 10 → 7)
  * Create Backorder / No Backorder radio dialog
  * cross-module round-trip back to PO + Create Bill + post

Seeded state:
  - Vendor 'Bench Supply Co' (supplier_rank=1).
  - Two storable products 'Bench PO Item A' (20.00) and 'Bench PO Item B'
    (40.00) with vendor supplierinfo pinning the purchase price.
  - NO PO — the agent creates it during the task.
  - A distractor vendor 'Bench Filler Vendor' with one distractor draft
    RFQ so the Purchase list isn't empty on first load (helps the agent
    identify the 'New' affordance; also tests that the agent doesn't
    accidentally modify an unrelated RFQ).

The check.py enforces ALL THREE endpoints:
  1. A purchase.order exists for Bench Supply Co, state='purchase', with
     exactly 2 lines (A qty=10, B qty=5) and qty_received 7 / 5.
  2. Exactly one stock.picking with state='done' and a backorder child
     carrying 3 remaining Item A units.
  3. Exactly one posted account.move (move_type='in_invoice') with
     ref='BSC-BILL-3WM' referencing that PO.
"""


VENDOR_NAME = "Bench Supply Co"
DISTRACTOR_VENDOR = "Bench Filler Vendor"
PRODUCT_A = "Bench PO Item A"
PRODUCT_B = "Bench PO Item B"
PRICE_A = 20.0
PRICE_B = 40.0
BILL_REF = "BSC-BILL-3WM"
DISTRACTOR_REF = "R-BENCH-FILLER-001"


def _cleanup(env):
    """Scrub prior runs — POs, receipts, bills, products."""
    # Vendor bills with our ref.
    bills = env["account.move"].with_context(active_test=False).search([
        ("ref", "=", BILL_REF),
        ("move_type", "=", "in_invoice"),
    ])
    for b in bills:
        try:
            if b.state == "posted":
                b.button_draft()
            b.button_cancel()
        except Exception:
            pass
        try:
            b.unlink()
        except Exception:
            pass

    # POs for our vendor (target and distractor).
    vendor_names = [VENDOR_NAME, DISTRACTOR_VENDOR]
    pos = env["purchase.order"].with_context(active_test=False).search([
        ("partner_id.name", "in", vendor_names),
    ])
    for po in pos:
        # Cascade-kill any bills attached to the PO.
        attached_bills = po.invoice_ids
        for b in attached_bills:
            try:
                if b.state == "posted":
                    b.button_draft()
                b.button_cancel()
                b.unlink()
            except Exception:
                pass
        # Pickings linked to PO.
        for p in po.picking_ids:
            if p.state not in ("done", "cancel"):
                try:
                    p.action_cancel()
                except Exception:
                    pass
            try:
                p.move_ids.write({"state": "cancel"})
                p.write({"state": "cancel"})
                p.unlink()
            except Exception:
                pass
        try:
            if po.state in ("purchase", "done"):
                po.button_cancel()
            po.unlink()
        except Exception:
            pass

    # Products — unlink the templates if no other PO/SO still references
    # the variants.
    prods = env["product.product"].search([("name", "in", [PRODUCT_A, PRODUCT_B])])
    for p in prods:
        try:
            env["stock.move.line"].search([("product_id", "=", p.id)]).unlink()
            env["stock.move"].search([("product_id", "=", p.id)]).unlink()
            env["product.supplierinfo"].search([("product_tmpl_id", "=", p.product_tmpl_id.id)]).unlink()
        except Exception:
            pass
    try:
        prods.mapped("product_tmpl_id").unlink()
    except Exception:
        pass


def _ensure_vendor(env, name, email):
    vendor = env["res.partner"].search([("name", "=", name)], limit=1)
    if not vendor:
        vendor = env["res.partner"].create({
            "name": name,
            "email": email,
            "company_type": "company",
            "supplier_rank": 1,
        })
    else:
        vendor.write({"supplier_rank": max(vendor.supplier_rank, 1)})
    return vendor


def _ensure_product(env, name, price, vendor):
    """Create a storable product with a vendor supplierinfo pinning price."""
    prod = env["product.product"].search([("name", "=", name)], limit=1)
    if prod:
        prod.product_tmpl_id.write({
            "list_price": price,
            "standard_price": price,
        })
        return prod
    tmpl = env["product.template"].create({
        "name": name,
        # 'consu' + is_storable=True gives stockable behaviour (Odoo 19
        # merged 'product' type into 'consu' + is_storable switch).
        "type": "consu",
        "is_storable": True,
        "tracking": "none",
        "list_price": price,
        "standard_price": price,
        "purchase_ok": True,
        "purchase_method": "receive",  # 3-way match: bill what was received
        "invoice_policy": "delivery",
    })
    env["product.supplierinfo"].create({
        "partner_id": vendor.id,
        "product_tmpl_id": tmpl.id,
        "price": price,
        "min_qty": 0,
    })
    return tmpl.product_variant_id


def setup(env):
    _cleanup(env)

    admin = env.ref("base.user_admin")
    # Needed so the receipt Operations tab / multi-location features
    # behave consistently with the scrap / multi-loc benchmark base.
    admin.group_ids |= env.ref("stock.group_stock_multi_locations")

    # --- Vendors -------------------------------------------------------
    vendor = _ensure_vendor(env, VENDOR_NAME, "orders@benchsupply.example")
    distractor_vendor = _ensure_vendor(
        env, DISTRACTOR_VENDOR, "filler@benchfiller.example"
    )

    # --- Products ------------------------------------------------------
    prod_a = _ensure_product(env, PRODUCT_A, PRICE_A, vendor)
    prod_b = _ensure_product(env, PRODUCT_B, PRICE_B, vendor)

    # --- Distractor draft RFQ so the Purchase list is populated --------
    # The agent should ignore this RFQ completely.
    distractor = env["purchase.order"].create({
        "partner_id": distractor_vendor.id,
        "partner_ref": DISTRACTOR_REF,
    })
    env["purchase.order.line"].create({
        "order_id": distractor.id,
        "product_id": prod_a.id,
        "product_qty": 1,
        "price_unit": PRICE_A,
        "name": PRODUCT_A,
        "tax_ids": [(5, 0, 0)],
    })

    env.cr.commit()
