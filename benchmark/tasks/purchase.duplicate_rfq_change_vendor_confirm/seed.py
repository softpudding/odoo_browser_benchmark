"""Seed a draft RFQ for the duplicate-change-vendor-confirm task.

Category 2 (MEDIUM): The agent must duplicate an RFQ via the Action
menu, swap its vendor, and confirm the copy. Capability tested:
Duplicate action in Purchase + vendor swap + confirm without touching
the original RFQ.
"""


def setup(env):
    # --- Ensure vendors ---
    meridian = env["res.partner"].search(
        [("name", "=", "Meridian Supply Co")], limit=1
    )
    if not meridian:
        meridian = env["res.partner"].create({
            "name": "Meridian Supply Co",
            "email": "orders@meridiansupply.com",
            "supplier_rank": 1,
        })
    else:
        meridian.write({"supplier_rank": max(meridian.supplier_rank, 1)})

    pinnacle = env["res.partner"].search(
        [("name", "=", "Pinnacle Hardware")], limit=1
    )
    if not pinnacle:
        pinnacle = env["res.partner"].create({
            "name": "Pinnacle Hardware",
            "email": "sales@pinnaclehardware.com",
            "supplier_rank": 1,
        })
    else:
        pinnacle.write({"supplier_rank": max(pinnacle.supplier_rank, 1)})

    # --- Cleanup prior runs ---
    old_orders = env["purchase.order"].search([
        ("partner_ref", "in", ["BENCH-RFQ-DUP", "PH-REISSUE-77"]),
    ])
    for order in old_orders:
        if order.state in ("purchase", "done"):
            order.button_cancel()
        order.unlink()

    # --- Ensure products exist ---
    products = {}
    for name, price in [("Rubber Gasket", 1.50), ("Stainless Bolt M8", 0.75)]:
        p = env["product.product"].search([("name", "=", name)], limit=1)
        if not p:
            tmpl = env["product.template"].create({
                "name": name,
                "type": "consu",
                "list_price": price,
                "standard_price": price,
                "purchase_ok": True,
            })
            p = tmpl.product_variant_id
        products[name] = p

    # --- Create the source draft RFQ ---
    po = env["purchase.order"].create({
        "partner_id": meridian.id,
        "partner_ref": "BENCH-RFQ-DUP",
    })

    env["purchase.order.line"].create({
        "order_id": po.id,
        "product_id": products["Rubber Gasket"].id,
        "product_qty": 200,
        "price_unit": 1.50,
        "name": "Rubber Gasket",
        "taxes_id": [(5, 0, 0)],
    })
    env["purchase.order.line"].create({
        "order_id": po.id,
        "product_id": products["Stainless Bolt M8"].id,
        "product_qty": 500,
        "price_unit": 0.75,
        "name": "Stainless Bolt M8",
        "taxes_id": [(5, 0, 0)],
    })
