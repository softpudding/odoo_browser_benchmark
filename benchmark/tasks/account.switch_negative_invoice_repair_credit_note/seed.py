"""Seed draft invoices for a credit-note repair task."""


def setup(env):
    discount_group = env.ref("sale.group_discount_per_so_line", raise_if_not_found=False)
    admin = env.ref("base.user_admin")
    if discount_group:
        admin.write({"group_ids": [(4, discount_group.id)]})

    partner = env["res.partner"].search([("name", "=", "Lumen Works")], limit=1)
    if not partner:
        partner = env["res.partner"].create({
            "name": "Lumen Works",
            "email": "lumen@example.com",
        })

    product_specs = [
        ("Return Fee", 120.0, "Qty=1 | Discount=0"),
        ("Service Retainer", 80.0, "Qty=2 | Discount=10"),
        ("Restocking Surcharge", 60.0, "Qty=1 | Discount=5"),
        ("Compliance Credit", 95.0, "Qty=1 | Discount=0"),
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

    moves = env["account.move"].search([
        ("partner_id", "=", partner.id),
        ("move_type", "in", ["out_invoice", "out_refund"]),
    ])
    posted = moves.filtered(lambda move: move.state == "posted")
    if posted:
        posted.button_draft()
    moves.unlink()

    def make_invoice(origin, line_specs):
        return env["account.move"].create({
            "move_type": "out_invoice",
            "partner_id": partner.id,
            "invoice_origin": origin,
            "invoice_date": "2026-04-10",
            "invoice_line_ids": [
                (0, 0, {
                    "product_id": products[product_name].id,
                    "quantity": qty,
                    "price_unit": price_unit,
                    "discount": discount,
                    "name": label,
                })
                for product_name, qty, price_unit, discount, label in line_specs
            ],
        })

    make_invoice(
        "RET-507",
        [
            ("Compliance Credit", 1, -95.0, 0.0, "Leave this invoice untouched"),
        ],
    )

    make_invoice(
        "RET-508",
        [
            ("Return Fee", 1, -120.0, 0.0, "Placeholder return line"),
            ("Service Retainer", 3, -80.0, 0.0, "Placeholder service line"),
            ("Restocking Surcharge", 1, -60.0, 15.0, "Placeholder surcharge line"),
        ],
    )
