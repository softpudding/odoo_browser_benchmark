"""Seed for purchase.confirm_rfq_receive_full_three_way_match (MEDIUM).

Category: closed_loop_cross_module.

Workflow (agent):
  - Open seeded draft RFQ BENCH-RFQ-3WAY-2 for vendor 'Bench Supplier Inc'.
  - Click Confirm Order (statusbar) -> PO state flips to 'purchase'.
  - Click Receive Products smart button -> opens auto-generated
    stock.picking in Ready state.
  - Click Validate -> picking state flips to 'done'; PO invoice_status
    becomes 'to invoice'.

This stops at receipt validation — no vendor bill is created.  The
3-way match is READY (goods received, no bill yet).  Differs from
purchase.create_rfq_receive_invoice_3way_match (row 397) which goes all
the way to posting a vendor bill, and from purchase_stock.confirm_rfq_receive_full
which uses a different vendor / reference / product set and does not
assert invoice_status.

Hard aspects (medium-tier):
  - PO form statusbar Confirm Order (not the list checkbox flow).
  - Smart-button navigation to the receipt.
  - Validate on the receipt (no backorder dialog — full receipt).
"""


VENDOR_NAME = "Bench Supplier Inc"
VENDOR_EMAIL = "orders@benchsupplier.example.com"
RFQ_REF = "BENCH-RFQ-3WAY-2"
PRODUCT_A = "Bench 3WM Bracket"
PRODUCT_B = "Bench 3WM Fastener Kit"
PRICE_A = 25.0
PRICE_B = 5.0
QTY_A = 8.0
QTY_B = 12.0


def _cleanup(env):
    """Scrub any lingering records from prior runs."""
    # Vendor bills referencing our PO (just in case an earlier run
    # accidentally created one).
    bills = env["account.move"].with_context(active_test=False).search([
        ("move_type", "=", "in_invoice"),
        ("partner_id.name", "=", VENDOR_NAME),
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

    pos = env["purchase.order"].with_context(active_test=False).search([
        ("partner_id.name", "=", VENDOR_NAME),
    ])
    for po in pos:
        for bill in po.invoice_ids:
            try:
                if bill.state == "posted":
                    bill.button_draft()
                bill.button_cancel()
                bill.unlink()
            except Exception:
                pass
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

    # Drop products so re-seeding can re-register storable flag cleanly.
    prods = env["product.product"].search([("name", "in", [PRODUCT_A, PRODUCT_B])])
    for p in prods:
        try:
            env["stock.move.line"].search([("product_id", "=", p.id)]).unlink()
            env["stock.move"].search([("product_id", "=", p.id)]).unlink()
            env["product.supplierinfo"].search([
                ("product_tmpl_id", "=", p.product_tmpl_id.id)
            ]).unlink()
        except Exception:
            pass
    try:
        prods.mapped("product_tmpl_id").unlink()
    except Exception:
        pass


def _ensure_vendor(env):
    vendor = env["res.partner"].search([("name", "=", VENDOR_NAME)], limit=1)
    if not vendor:
        vendor = env["res.partner"].create({
            "name": VENDOR_NAME,
            "email": VENDOR_EMAIL,
            "company_type": "company",
            "supplier_rank": 1,
        })
    else:
        vendor.write({"supplier_rank": max(vendor.supplier_rank, 1)})
    return vendor


def _ensure_product(env, name, price):
    """Create a storable product with purchase_method='receive' for 3-way match."""
    prod = env["product.product"].search([("name", "=", name)], limit=1)
    if prod:
        prod.product_tmpl_id.write({
            "list_price": price,
            "standard_price": price,
            "purchase_method": "receive",
        })
        return prod
    tmpl = env["product.template"].create({
        "name": name,
        # Odoo 19: 'consu' + is_storable=True gives a storable product.
        "type": "consu",
        "is_storable": True,
        "tracking": "none",
        "list_price": price,
        "standard_price": price,
        "purchase_ok": True,
        "purchase_method": "receive",  # 3-way match: bill what was received
        "invoice_policy": "delivery",
    })
    return tmpl.product_variant_id


def setup(env):
    _cleanup(env)

    vendor = _ensure_vendor(env)
    prod_a = _ensure_product(env, PRODUCT_A, PRICE_A)
    prod_b = _ensure_product(env, PRODUCT_B, PRICE_B)

    po = env["purchase.order"].create({
        "partner_id": vendor.id,
        "partner_ref": RFQ_REF,
        "origin": RFQ_REF,
    })
    env["purchase.order.line"].create({
        "order_id": po.id,
        "product_id": prod_a.id,
        "product_qty": QTY_A,
        "price_unit": PRICE_A,
        "name": PRODUCT_A,
        "tax_ids": [(5, 0, 0)],
    })
    env["purchase.order.line"].create({
        "order_id": po.id,
        "product_id": prod_b.id,
        "product_qty": QTY_B,
        "price_unit": PRICE_B,
        "name": PRODUCT_B,
        "tax_ids": [(5, 0, 0)],
    })

    env.cr.commit()
