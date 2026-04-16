"""Seed a draft RFQ for the confirm-rfq task."""

TARGET_VENDOR = "Nimbus Industrial Supply"
TARGET_SOURCE = "BENCH-CONFIRM-01"
PRODUCT_NAME = "Precision Fastener Set"


def setup(env):
    vendor = env["res.partner"].search([("name", "=", TARGET_VENDOR)], limit=1)
    if vendor:
        env["purchase.order"].search([
            ("partner_id", "=", vendor.id),
            ("origin", "=", TARGET_SOURCE),
        ]).unlink()

    if not vendor:
        vendor = env["res.partner"].create({
            "name": TARGET_VENDOR,
            "email": "purchasing@nimbus-industrial.example.com",
            "supplier_rank": 1,
        })
    else:
        vendor.write({"supplier_rank": 1})

    product = env["product.product"].search([("name", "=", PRODUCT_NAME)], limit=1)
    if not product:
        tmpl = env["product.template"].create({
            "name": PRODUCT_NAME,
            "type": "consu",
            "list_price": 24.0,
            "standard_price": 24.0,
        })
        product = tmpl.product_variant_id

    po = env["purchase.order"].create({
        "partner_id": vendor.id,
        "origin": TARGET_SOURCE,
    })
    env["purchase.order.line"].create({
        "order_id": po.id,
        "product_id": product.id,
        "product_qty": 6,
        "price_unit": 24.0,
        "name": PRODUCT_NAME,
    })
