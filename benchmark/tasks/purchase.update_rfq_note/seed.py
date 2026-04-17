"""Seed an RFQ for the RFQ note update task."""

VENDOR_NAME = "Apex Supply Co."
ORDER_REF = "BENCH-NOTE-01"
PRODUCT_NAME = "Copper Lock Washer"


def setup(env):
    env["purchase.order"].search([("origin", "=", ORDER_REF)]).unlink()

    vendor = env["res.partner"].search([("name", "=", VENDOR_NAME)], limit=1)
    if not vendor:
        vendor = env["res.partner"].create({
            "name": VENDOR_NAME,
            "email": "procurement@apex.example.com",
            "supplier_rank": 1,
        })
    else:
        vendor.write({"supplier_rank": 1})

    product = env["product.product"].search([("name", "=", PRODUCT_NAME)], limit=1)
    if not product:
        tmpl = env["product.template"].create({
            "name": PRODUCT_NAME,
            "type": "consu",
            "list_price": 4.5,
        })
        product = tmpl.product_variant_id

    rfq = env["purchase.order"].create({
        "partner_id": vendor.id,
        "origin": ORDER_REF,
        "note": "Initial supplier review pending.",
    })

    env["purchase.order.line"].create({
        "order_id": rfq.id,
        "product_id": product.id,
        "product_qty": 20,
        "price_unit": 4.5,
        "name": PRODUCT_NAME,
    })
