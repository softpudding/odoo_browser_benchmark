"""Seed draft invoices for a credit-note recovery task."""


def setup(env):
    partner = env["res.partner"].search([("name", "=", "Lumen Works")], limit=1)
    if not partner:
        partner = env["res.partner"].create({
            "name": "Lumen Works",
            "email": "lumen@example.com",
        })

    products = {}
    for name, price in [("Return Fee", 120.0), ("Service Retainer", 80.0)]:
        product = env["product.product"].search([("name", "=", name)], limit=1)
        if not product:
            template = env["product.template"].create({
                "name": name,
                "type": "consu",
                "list_price": price,
            })
            product = template.product_variant_id
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
                    "name": label,
                })
                for product_name, qty, price_unit, label in line_specs
            ],
        })

    make_invoice(
        "RET-203",
        [
            ("Service Retainer", 1, 80.0, "Leave this invoice untouched"),
        ],
    )

    make_invoice(
        "RET-204",
        [
            ("Return Fee", 1, -120.0, "Return fee adjustment"),
        ],
    )


