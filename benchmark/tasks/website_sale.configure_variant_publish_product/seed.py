"""Seed data for website_sale.configure_variant_publish_product."""


PRODUCT_NAME = "Field Pack Duffel"
ATTRIBUTE_NAME = "Bench Size"
VALUE_NAMES = ["Carry-On", "Weekender"]


def setup(env):
    product = env["product.template"].search([("name", "=", PRODUCT_NAME)], limit=1)
    if not product:
        product = env["product.template"].create({
            "name": PRODUCT_NAME,
            "type": "consu",
            "list_price": 129.0,
            "website_published": False,
            "sale_ok": True,
        })
    else:
        product.write({
            "list_price": 129.0,
            "website_published": False,
            "attribute_line_ids": [(5, 0, 0)],
        })

    attribute = env["product.attribute"].search([("name", "=", ATTRIBUTE_NAME)], limit=1)
    if not attribute:
        attribute = env["product.attribute"].create({
            "name": ATTRIBUTE_NAME,
            "create_variant": "always",
        })
    values = env["product.attribute.value"]
    for value_name in VALUE_NAMES:
        value = env["product.attribute.value"].search([
            ("name", "=", value_name),
            ("attribute_id", "=", attribute.id),
        ], limit=1)
        if not value:
            value = env["product.attribute.value"].create({
                "name": value_name,
                "attribute_id": attribute.id,
            })
        values |= value
    product.write({"website_published": False, "attribute_line_ids": [(5, 0, 0)]})
