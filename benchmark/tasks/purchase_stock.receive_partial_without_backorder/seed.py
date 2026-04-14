"""Seed a confirmed PO for a partial receipt without backorder task.

Category 2: Policy trap (wizard).
The agent must validate a partial receipt, then use the backorder
wizard's non-default no-backorder path.
"""


TARGET_ORIGIN = "NOBACK-04"


def setup(env):
    vendor = env["res.partner"].search([("name", "=", "North Coast Components")], limit=1)
    if not vendor:
        vendor = env["res.partner"].create({
            "name": "North Coast Components",
            "email": "receiving@northcoast.example.com",
            "supplier_rank": 1,
        })
    else:
        vendor.write({"supplier_rank": 1})

    products = {}
    for name, price in [("Servo Motor", 230.0), ("Sensor Harness", 18.0)]:
        product = env["product.product"].search([("name", "=", name)], limit=1)
        if not product:
            template = env["product.template"].create({
                "name": name,
                "type": "consu",
                "list_price": price,
                "standard_price": price,
            })
            product = template.product_variant_id
        products[name] = product

    old_pos = env["purchase.order"].search([
        ("partner_id", "=", vendor.id),
        ("origin", "=", TARGET_ORIGIN),
    ])
    for po in old_pos:
        for pick in po.picking_ids.filtered(lambda p: p.state not in ("done", "cancel")):
            pick.action_cancel()
        if po.state in ("purchase", "done"):
            po.button_cancel()
        if po.state == "cancel":
            po.button_draft()
        po.unlink()

    po = env["purchase.order"].create({
        "partner_id": vendor.id,
        "origin": TARGET_ORIGIN,
    })
    env["purchase.order.line"].create({
        "order_id": po.id,
        "product_id": products["Servo Motor"].id,
        "product_qty": 8,
        "price_unit": 230.0,
        "name": "Servo Motor",
    })
    env["purchase.order.line"].create({
        "order_id": po.id,
        "product_id": products["Sensor Harness"].id,
        "product_qty": 12,
        "price_unit": 18.0,
        "name": "Sensor Harness",
    })
    po.button_confirm()
