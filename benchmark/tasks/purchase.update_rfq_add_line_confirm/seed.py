"""Seed a draft RFQ for the update-rfq-add-line-confirm task.

Category 2 (MEDIUM): Add a product line to an existing RFQ, change the
order deadline, and confirm. Requires line addition + date picker + confirm.
"""

VENDOR_NAME = "Pinnacle Hardware"
RFQ_REF = "BENCH-RFQ-UPD"


def setup(env):
    # --- Cleanup prior runs ---
    vendor = env["res.partner"].search(
        [("name", "=", VENDOR_NAME)], limit=1
    )
    if not vendor:
        vendor = env["res.partner"].create({
            "name": VENDOR_NAME,
            "email": "orders@pinnaclehw.com",
            "supplier_rank": 1,
        })
    else:
        vendor.write({"supplier_rank": max(vendor.supplier_rank, 1)})

    old_pos = env["purchase.order"].search([
        ("partner_id", "=", vendor.id),
        ("partner_ref", "=", RFQ_REF),
    ])
    for po in old_pos:
        if po.state in ("purchase", "done"):
            po.button_cancel()
        if po.state == "cancel":
            po.unlink()
        elif po.state in ("draft", "sent"):
            po.unlink()

    # Also clean by origin
    old_pos2 = env["purchase.order"].search([
        ("origin", "=", RFQ_REF),
    ])
    for po in old_pos2:
        if po.state in ("purchase", "done"):
            po.button_cancel()
        if po.state == "cancel":
            po.unlink()
        elif po.state in ("draft", "sent"):
            po.unlink()

    # --- Ensure products exist ---
    products = {}
    for name, price in [
        ("Rubber Gasket", 1.50),
        ("Stainless Bolt M8", 0.75),
        ("Hex Wrench Set", 15.00),
    ]:
        p = env["product.product"].search([("name", "=", name)], limit=1)
        if not p:
            tmpl = env["product.template"].create({
                "name": name,
                "type": "consu",
                "list_price": price,
                "standard_price": price,
            })
            p = tmpl.product_variant_id
        products[name] = p

    # --- Create draft RFQ with 2 existing lines ---
    po = env["purchase.order"].create({
        "partner_id": vendor.id,
        "partner_ref": RFQ_REF,
        "origin": RFQ_REF,
    })

    env["purchase.order.line"].create({
        "order_id": po.id,
        "product_id": products["Rubber Gasket"].id,
        "product_qty": 200,
        "price_unit": 1.50,
        "tax_ids": [(5, 0, 0)],
    })
    env["purchase.order.line"].create({
        "order_id": po.id,
        "product_id": products["Stainless Bolt M8"].id,
        "product_qty": 500,
        "price_unit": 0.75,
        "tax_ids": [(5, 0, 0)],
    })
