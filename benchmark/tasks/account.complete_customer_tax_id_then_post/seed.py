"""Seed invoices that require repairing customer metadata before posting."""


def setup(env):
    east = env["res.partner"].create({
        "name": "Northwind Studio East",
        "email": "east@northwind.example.com",
        "vat": False,
    })
    west = env["res.partner"].create({
        "name": "Northwind Studio West",
        "email": "west@northwind.example.com",
        "vat": False,
    })

    products = {}
    for name, price in [("Governance Pack", 180.0), ("Compliance Review", 95.0)]:
        product = env["product.product"].search([("name", "=", name)], limit=1)
        if not product:
            template = env["product.template"].create({
                "name": name,
                "type": "consu",
                "list_price": price,
            })
            product = template.product_variant_id
        products[name] = product

    def make_invoice(partner, origin, narration, line_specs):
        return env["account.move"].create({
            "move_type": "out_invoice",
            "partner_id": partner.id,
            "invoice_origin": origin,
            "invoice_date": "2026-04-10",
            "narration": narration,
            "invoice_line_ids": [
                (0, 0, {
                    "product_id": products[product_name].id,
                    "quantity": qty,
                    "price_unit": price_unit,
                    "name": label,
                })
                for product_name, qty, price_unit, label in line_specs
            ],
        })

    make_invoice(
        west,
        "VAT-303",
        "Target VAT: EU3031199",
        [
            ("Compliance Review", 1, 95.0, "Leave this invoice untouched"),
        ],
    )

    make_invoice(
        east,
        "VAT-302",
        "Target VAT: EU3029981",
        [
            ("Governance Pack", 1, 180.0, "Governance package"),
        ],
    )


