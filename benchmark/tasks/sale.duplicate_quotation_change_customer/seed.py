"""Seed a draft quotation for the duplicate-and-change-customer task.

Category 2 (MEDIUM): The agent must duplicate a quotation via the
Action menu and reassign the copy to a different customer. Capability
tested: Duplicate action + relational field swap, leaving the original
untouched.
"""


def setup(env):
    # --- Ensure partners ---
    azure = env["res.partner"].search(
        [("name", "=", "Azure Interior")], limit=1
    )
    if not azure:
        azure = env["res.partner"].create({
            "name": "Azure Interior",
            "email": "orders@azureinterior.com",
        })

    summit = env["res.partner"].search(
        [("name", "=", "Summit Ventures")], limit=1
    )
    if not summit:
        summit = env["res.partner"].create({
            "name": "Summit Ventures",
            "email": "hello@summitventures.com",
        })

    # --- Cleanup prior runs ---
    old_orders = env["sale.order"].search([
        ("client_order_ref", "in", ["BENCH-DUP-01", "SV-DUP-2026"]),
    ])
    for order in old_orders:
        if order.state == "sale":
            order.action_cancel()
        order.unlink()

    # --- Ensure products exist ---
    products = {}
    for name, price in [("Ergo Chair", 260.0), ("Desk Lamp", 45.0)]:
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

    # --- Create the source draft quotation ---
    admin = env.ref("base.user_admin")
    so = env["sale.order"].create({
        "partner_id": azure.id,
        "user_id": admin.id,
        "client_order_ref": "BENCH-DUP-01",
    })

    env["sale.order.line"].create({
        "order_id": so.id,
        "product_id": products["Ergo Chair"].id,
        "product_uom_qty": 3,
        "price_unit": 260.0,
        "tax_ids": [(5, 0, 0)],
    })
    env["sale.order.line"].create({
        "order_id": so.id,
        "product_id": products["Desk Lamp"].id,
        "product_uom_qty": 4,
        "price_unit": 45.0,
        "tax_ids": [(5, 0, 0)],
    })
