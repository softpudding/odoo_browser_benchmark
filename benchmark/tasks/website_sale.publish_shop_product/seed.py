"""Seed an unpublished storable product for the Shop publish task."""


PRODUCT_NAME = "Shop Special Chair"


def setup(env):
    env["product.template"].search([("name", "=", PRODUCT_NAME)]).unlink()

    env["product.template"].create({
        "name": PRODUCT_NAME,
        "is_storable": True,
        "sale_ok": True,
        "purchase_ok": False,
        "list_price": 0.0,
        "is_published": False,
        "description_ecommerce": False,
    })
