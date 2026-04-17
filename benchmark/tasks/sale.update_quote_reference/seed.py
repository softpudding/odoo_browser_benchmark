"""Seed a quotation for the customer-reference update task."""

CUSTOMER_NAME = "Summitline Software"
REFERENCE = "BENCH-QREF-01"
PRODUCT_NAME = "Consulting Services"


def setup(env):
    env["sale.order"].search([("client_order_ref", "=", REFERENCE)]).unlink()

    partner = env["res.partner"].search([("name", "=", CUSTOMER_NAME)], limit=1)
    if not partner:
        partner = env["res.partner"].create({
            "name": CUSTOMER_NAME,
            "email": "accounts@summitline.example.com",
        })

    user_admin = env.ref("base.user_admin")
    product = env["product.product"].search([("name", "=", PRODUCT_NAME)], limit=1)
    if not product:
        tmpl = env["product.template"].create({
            "name": PRODUCT_NAME,
            "type": "service",
            "invoice_policy": "order",
        })
        product = tmpl.product_variant_id

    env["sale.order"].create({
        "partner_id": partner.id,
        "user_id": user_admin.id,
        "client_order_ref": REFERENCE,
        "state": "draft",
        "order_line": [
            (0, 0, {
                "product_id": product.id,
                "product_uom_qty": 1,
                "price_unit": 150.0,
                "name": PRODUCT_NAME,
            }),
        ],
    })
