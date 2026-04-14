"""Seed quotations for a dense inline-editing sales task."""


def setup(env):
    discount_group = env.ref("sale.group_discount_per_so_line", raise_if_not_found=False)
    admin = env.ref("base.user_admin")
    if discount_group:
        admin.write({"group_ids": [(4, discount_group.id)]})

    partner = env["res.partner"].search([("name", "=", "Aurora Interiors")], limit=1)
    if not partner:
        partner = env["res.partner"].create({
            "name": "Aurora Interiors",
            "email": "aurora@example.com",
        })

    payment_term = env["account.payment.term"].search([("name", "=", "15 Days")], limit=1)
    if not payment_term:
        payment_term = env["account.payment.term"].create({"name": "15 Days"})

    product_specs = [
        (
            "Standing Desk",
            450.0,
            "Use line description: Ergonomic standing desk bundle. Apply discount: 5%.",
        ),
        (
            "Office Chair",
            150.0,
            "Use line description: Mesh chair support package. Apply discount: 10%.",
        ),
        (
            "Whiteboard",
            80.0,
            "Use line description: Magnetic planning board. Apply discount: 0%.",
        ),
        (
            "Desk Lamp",
            45.0,
            "Use line description: Adjustable desk lamp. Apply discount: 0%.",
        ),
    ]

    products = {}
    for name, price, description_sale in product_specs:
        product = env["product.product"].search([("name", "=", name)], limit=1)
        if not product:
            template = env["product.template"].create({
                "name": name,
                "type": "consu",
                "list_price": price,
                "description_sale": description_sale,
            })
            product = template.product_variant_id
        else:
            product.product_tmpl_id.write({
                "list_price": price,
                "description_sale": description_sale,
            })
        products[name] = product

    env["sale.order"].search([("partner_id", "=", partner.id)]).unlink()

    def make_order(order_name, customer_ref, lines):
        order = env["sale.order"].create({
            "name": order_name,
            "partner_id": partner.id,
            "user_id": admin.id,
            "client_order_ref": customer_ref,
        })
        for product_name, qty, price, line_name in lines:
            env["sale.order.line"].create({
                "order_id": order.id,
                "product_id": products[product_name].id,
                "product_uom_qty": qty,
                "price_unit": price,
                "name": line_name,
                "discount": 0.0,
            })
        return order

    make_order(
        "AUR-ALT1",
        "OPS-041",
        [
            ("Standing Desk", 1, 450.0, "Old desk placeholder"),
            ("Office Chair", 2, 150.0, "Old chair placeholder"),
        ],
    )

    make_order(
        "AUR-TGT",
        "OPS-042",
        [
            ("Standing Desk", 1, 450.0, "Placeholder desk line"),
            ("Office Chair", 2, 150.0, "Placeholder chair line"),
            ("Whiteboard", 1, 80.0, "Placeholder whiteboard line"),
        ],
    )

    make_order(
        "AUR-ALT2",
        "OPS-043",
        [
            ("Standing Desk", 1, 450.0, "Leave this quotation untouched"),
            ("Desk Lamp", 2, 45.0, "Leave this quotation untouched"),
        ],
    )

