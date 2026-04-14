"""Seed a confirmed PO with the wrong vendor.

Category 4: Recovery and rollback.
The PO is confirmed (locked), so the vendor cannot be edited inline.
The agent must cancel it and create a replacement PO with the correct vendor.
"""


def setup(env):
    # --- Vendors ---
    wrong_vendor = env["res.partner"].search([("name", "=", "Atlas Industrial")], limit=1)
    if not wrong_vendor:
        wrong_vendor = env["res.partner"].create({
            "name": "Atlas Industrial",
            "email": "sales@atlas.example.com",
            "supplier_rank": 1,
        })
    else:
        wrong_vendor.write({"supplier_rank": 1})

    correct_vendor = env["res.partner"].search([("name", "=", "Pinnacle Parts")], limit=1)
    if not correct_vendor:
        correct_vendor = env["res.partner"].create({
            "name": "Pinnacle Parts",
            "email": "orders@pinnacle.example.com",
            "supplier_rank": 1,
        })
    else:
        correct_vendor.write({"supplier_rank": 1})

    # --- Products ---
    products = {}
    for name, price in [("Hydraulic Pump", 340.0), ("Pressure Gauge", 85.0)]:
        p = env["product.product"].search([("name", "=", name)], limit=1)
        if not p:
            tmpl = env["product.template"].create({
                "name": name,
                "type": "consu",
                "list_price": price,
                "standard_price": price,
            })
            p = tmpl.product_variant_id
        else:
            p.product_tmpl_id.write({"standard_price": price})
        products[name] = p

    # --- Cleanup prior runs ---
    # Cancel and remove old wrong-vendor POs
    old_wrong = env["purchase.order"].search([
        ("partner_id", "=", wrong_vendor.id),
        ("origin", "=", "VENDOR-FIX-01"),
    ])
    for po in old_wrong:
        for pick in po.picking_ids.filtered(lambda p: p.state not in ("done", "cancel")):
            pick.action_cancel()
        if po.state in ("purchase", "done"):
            po.button_cancel()
        if po.state == "cancel":
            po.button_draft()
        po.unlink()

    # Remove any replacement POs from prior runs
    old_correct = env["purchase.order"].search([
        ("partner_id", "=", correct_vendor.id),
    ])
    for po in old_correct:
        for pick in po.picking_ids.filtered(lambda p: p.state not in ("done", "cancel")):
            pick.action_cancel()
        if po.state in ("purchase", "done"):
            po.button_cancel()
        if po.state == "cancel":
            po.button_draft()
        po.unlink()

    # --- Create confirmed PO with wrong vendor ---
    po = env["purchase.order"].create({
        "partner_id": wrong_vendor.id,
        "origin": "VENDOR-FIX-01",
    })
    env["purchase.order.line"].create({
        "order_id": po.id,
        "product_id": products["Hydraulic Pump"].id,
        "product_qty": 5,
        "price_unit": 340.0,
        "name": "Hydraulic Pump",
    })
    env["purchase.order.line"].create({
        "order_id": po.id,
        "product_id": products["Pressure Gauge"].id,
        "product_qty": 10,
        "price_unit": 85.0,
        "name": "Pressure Gauge",
    })
    po.button_confirm()
