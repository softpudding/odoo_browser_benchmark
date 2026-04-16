"""Seed a confirmed PO for the create-bill-from-po task.

Category 2 (MEDIUM): The agent must go from a confirmed PO into the
generated draft vendor bill via a stat/action button, set bill date and
reference, then confirm. Capability tested: cross-document creation
(Purchase → Accounting) plus date/reference entry.
"""


def setup(env):
    # --- Vendor ---
    vendor = env["res.partner"].search(
        [("name", "=", "Meridian Supply Co")], limit=1
    )
    if not vendor:
        vendor = env["res.partner"].create({
            "name": "Meridian Supply Co",
            "email": "billing@meridiansupply.com",
            "supplier_rank": 1,
        })
    else:
        vendor.write({"supplier_rank": max(vendor.supplier_rank, 1)})

    # --- Cleanup prior runs: remove draft/posted bills with our ref ---
    old_bills = env["account.move"].search([
        ("ref", "=", "MSC-BILL-9921"),
        ("move_type", "=", "in_invoice"),
    ])
    for bill in old_bills:
        if bill.state == "posted":
            bill.button_draft()
        bill.unlink()

    # Also remove any lingering PO with our ref
    old_pos = env["purchase.order"].search(
        [("partner_ref", "=", "BENCH-BILL-PO")]
    )
    for po in old_pos:
        if po.state in ("purchase", "done"):
            po.button_cancel()
        po.unlink()

    # --- Products: invoicing policy order so bills can be drawn ---
    products = {}
    for name, price in [("Cable Tray", 12.50), ("Junction Box", 8.00)]:
        p = env["product.product"].search([("name", "=", name)], limit=1)
        if not p:
            tmpl = env["product.template"].create({
                "name": name,
                "type": "consu",
                "list_price": price,
                "standard_price": price,
                "purchase_ok": True,
                "purchase_method": "purchase",
            })
            p = tmpl.product_variant_id
        else:
            p.product_tmpl_id.write({"purchase_method": "purchase"})
        products[name] = p

    # --- Create and confirm the PO ---
    po = env["purchase.order"].create({
        "partner_id": vendor.id,
        "partner_ref": "BENCH-BILL-PO",
    })
    env["purchase.order.line"].create({
        "order_id": po.id,
        "product_id": products["Cable Tray"].id,
        "product_qty": 50,
        "price_unit": 12.50,
        "name": "Cable Tray",
        "taxes_id": [(5, 0, 0)],
    })
    env["purchase.order.line"].create({
        "order_id": po.id,
        "product_id": products["Junction Box"].id,
        "product_qty": 40,
        "price_unit": 8.00,
        "name": "Junction Box",
        "taxes_id": [(5, 0, 0)],
    })
    po.button_confirm()
