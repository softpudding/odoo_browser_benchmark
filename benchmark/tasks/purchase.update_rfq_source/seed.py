"""Seed an RFQ for the source-document update task."""

VENDOR_NAME = "Horizon Components"
SOURCE = "BENCH-SRC-01"
PRODUCT_NAME = "Precision Sensor"
MARKER = "BENCH-RFQ-SOURCE-TASK"


def setup(env):
    env["purchase.order"].search([
        ("partner_ref", "=", MARKER),
    ]).unlink()

    vendor = env["res.partner"].search([("name", "=", VENDOR_NAME)], limit=1)
    if not vendor:
        vendor = env["res.partner"].create({
            "name": VENDOR_NAME,
            "email": "procurement@horizon.example.com",
            "supplier_rank": 1,
        })
    else:
        vendor.write({"supplier_rank": 1})

    product = env["product.product"].search([("name", "=", PRODUCT_NAME)], limit=1)
    if not product:
        tmpl = env["product.template"].create({
            "name": PRODUCT_NAME,
            "type": "consu",
            "list_price": 22.0,
        })
        product = tmpl.product_variant_id

    rfq = env["purchase.order"].create({
        "partner_id": vendor.id,
        "origin": SOURCE,
        "partner_ref": MARKER,
    })

    env["purchase.order.line"].create({
        "order_id": rfq.id,
        "product_id": product.id,
        "product_qty": 4,
        "price_unit": 22.0,
        "name": PRODUCT_NAME,
    })
