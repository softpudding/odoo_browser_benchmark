"""Seed a draft quotation for the add-discount-line task.

Category: deep_ui_interaction (EASY).
Starting state: Draft quotation BENCH-DISC-01 for Azure Interior with
Desk Organizer and Monitor Stand lines with 0% discount.
The agent must set discount to 10% on Desk Organizer line.
"""

ORDER_REF = "BENCH-DISC-01"


def setup(env):
    discount_group = env.ref("sale.group_discount_per_so_line", raise_if_not_found=False)
    admin = env.ref("base.user_admin")
    if discount_group:
        admin.write({"group_ids": [(4, discount_group.id)]})

    partner = env["res.partner"].search([("name", "=", "Azure Interior")], limit=1)
    if not partner:
        partner = env["res.partner"].create({
            "name": "Azure Interior",
            "email": "azure@example.com",
        })

    env["sale.order"].search([
        ("partner_id", "=", partner.id),
        ("client_order_ref", "=", ORDER_REF),
    ]).unlink()

    products = {}
    for name, price in [("Desk Organizer", 25.0), ("Monitor Stand", 85.0)]:
        p = env["product.product"].search([("name", "=", name)], limit=1)
        if not p:
            tmpl = env["product.template"].create({
                "name": name,
                "type": "consu",
                "list_price": price,
            })
            p = tmpl.product_variant_id
        products[name] = p

    so = env["sale.order"].create({
        "partner_id": partner.id,
        "user_id": admin.id,
        "client_order_ref": ORDER_REF,
    })

    env["sale.order.line"].create({
        "order_id": so.id,
        "product_id": products["Desk Organizer"].id,
        "product_uom_qty": 5,
        "price_unit": 25.0,
        "discount": 0.0,
        "tax_ids": [(5, 0, 0)],
    })

    env["sale.order.line"].create({
        "order_id": so.id,
        "product_id": products["Monitor Stand"].id,
        "product_uom_qty": 2,
        "price_unit": 85.0,
        "discount": 0.0,
        "tax_ids": [(5, 0, 0)],
    })