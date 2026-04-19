"""Cleanup for website_sale.configure_free_shipping_threshold."""


CARRIER_NAME = "Bench Ship"
PRODUCT_NAME = "Bench Ship Product"


def cleanup(env):
    carriers = env["delivery.carrier"].with_context(active_test=False).search([
        ("name", "=", CARRIER_NAME),
    ])
    if carriers:
        carriers.sudo().write({"active": False})
        env["delivery.price.rule"].with_context(active_test=False).search([
            ("carrier_id", "in", carriers.ids),
        ]).sudo().unlink()
        carriers.sudo().unlink()

    env["product.template"].with_context(active_test=False).search([
        ("name", "=", PRODUCT_NAME),
    ]).sudo().unlink()
