"""Seed a draft website product for an eCommerce publishing task."""


PRODUCT_NAME = "Summit Standing Desk"


def setup(env):
    env["product.template"].search([("name", "=", PRODUCT_NAME)]).unlink()

    env["product.template"].create({
        "name": PRODUCT_NAME,
        "type": "consu",
        "sale_ok": True,
        "purchase_ok": False,
        "list_price": 99.0,
        "is_published": False,
        "description_ecommerce": False,
    })
