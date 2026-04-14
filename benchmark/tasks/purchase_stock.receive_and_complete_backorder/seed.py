"""Seed a confirmed PO with two lines for partial receipt + backorder task.

Category 1: Closed-loop cross-module workflow.
The agent must navigate Purchase -> Inventory (receipt) -> backorder wizard
-> second receipt -> back to PO, handling the full receive cycle.
"""


def setup(env):
    # --- Vendor ---
    vendor = env["res.partner"].search([("name", "=", "Stellar Supplies")], limit=1)
    if not vendor:
        vendor = env["res.partner"].create({
            "name": "Stellar Supplies",
            "email": "info@stellarsupplies.example.com",
            "supplier_rank": 1,
        })
    else:
        vendor.write({"supplier_rank": 1})

    # --- Products ---
    products = {}
    for name, price in [("Copper Wire Spool", 45.0), ("Steel Bracket", 12.0)]:
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

    # --- Cleanup prior runs ---
    old_pos = env["purchase.order"].search([
        ("partner_id", "=", vendor.id),
        ("origin", "=", "BENCH-PARTIAL"),
    ])
    for po in old_pos:
        for pick in po.picking_ids:
            if pick.state not in ("done", "cancel"):
                pick.action_cancel()
            if pick.state != "done":
                pick.unlink()
        if po.state in ("purchase", "done"):
            po.button_cancel()
        if po.state == "cancel":
            po.button_draft()
        po.unlink()

    # --- Create and confirm PO ---
    po = env["purchase.order"].create({
        "partner_id": vendor.id,
        "origin": "BENCH-PARTIAL",
    })
    env["purchase.order.line"].create({
        "order_id": po.id,
        "product_id": products["Copper Wire Spool"].id,
        "product_qty": 10,
        "price_unit": 45.0,
        "name": "Copper Wire Spool",
    })
    env["purchase.order.line"].create({
        "order_id": po.id,
        "product_id": products["Steel Bracket"].id,
        "product_qty": 20,
        "price_unit": 12.0,
        "name": "Steel Bracket",
    })
    po.button_confirm()
