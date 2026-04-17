"""Seed a draft invoice for the update-invoice-reference task."""

PARTNER_NAME = "Asterline Consulting"
INVOICE_REF = "BENCH-INV-REF-01"
NEW_REF = "BENCH-INV-REF-01-UPDATED"
MARKER = "BENCH-INV-REF-TASK"


def setup(env):
    # Cleanup
    env["account.move"].search([
        ("invoice_origin", "=", MARKER),
        "|",
        ("ref", "=", INVOICE_REF),
        ("ref", "=", NEW_REF),
    ]).unlink()

    partner = env["res.partner"].search([("name", "=", PARTNER_NAME)], limit=1)
    if not partner:
        partner = env["res.partner"].create({
            "name": PARTNER_NAME,
            "email": "billing@asterline.example.com",
        })

    product = env["product.product"].search([("name", "=", "Consulting Services")], limit=1)
    if not product:
        tmpl = env["product.template"].create({
            "name": "Consulting Services",
            "type": "service",
            "list_price": 600.0,
            "invoice_policy": "order",
        })
        product = tmpl.product_variant_id

    env["account.move"].create({
        "move_type": "out_invoice",
        "partner_id": partner.id,
        "ref": INVOICE_REF,
        "invoice_origin": MARKER,
        "invoice_date": "2026-04-16",
        "invoice_line_ids": [
            (0, 0, {
                "product_id": product.id,
                "quantity": 1,
                "price_unit": 600.0,
                "name": "Consulting services",
                "tax_ids": [(5, 0, 0)],
            }),
        ],
    })
