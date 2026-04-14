"""Seed draft customer invoices for an accounting repair task."""


def setup(env):
    partner = env["res.partner"].search([("name", "=", "Beacon Design")], limit=1)
    if not partner:
        partner = env["res.partner"].create({
            "name": "Beacon Design",
            "email": "beacon@example.com",
        })

    product_specs = [
        ("Acoustic Panel", 220.0, "Qty=2 | Discount=5"),
        ("Focus Lamp", 140.0, "Qty=1 | Discount=15"),
        ("Desk Shelf", 90.0, "Qty=3 | Discount=0"),
        ("Visitor Chair", 175.0, "Qty=2 | Discount=0"),
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

    env["account.move"].search([
        ("partner_id", "=", partner.id),
        ("move_type", "=", "out_invoice"),
    ]).button_draft()
    env["account.move"].search([
        ("partner_id", "=", partner.id),
        ("move_type", "=", "out_invoice"),
    ]).unlink()

    def make_invoice(origin, line_specs):
        move = env["account.move"].create({
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
        move.write({"ref": False})
        return move

    make_invoice(
        "APR-ARCHIVE",
        [
            ("Visitor Chair", 2, 175.0, 0.0, "Archive invoice line"),
        ],
    )

    make_invoice(
        "APR-OPS",
        [
            ("Acoustic Panel", 1, 220.0, 0.0, "Placeholder acoustic line"),
            ("Focus Lamp", 3, 140.0, 0.0, "Placeholder lamp line"),
            ("Desk Shelf", 1, 90.0, 10.0, "Placeholder shelf line"),
        ],
    )


