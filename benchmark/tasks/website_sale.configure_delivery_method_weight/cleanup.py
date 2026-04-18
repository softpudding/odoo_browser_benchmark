"""Cleanup for website_sale.configure_delivery_method_weight."""


CARRIER_NAME = "Bench Weight Shipping"
DELIVERY_PRODUCT_NAME = "Bench Delivery Product"


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
        ("name", "=", DELIVERY_PRODUCT_NAME),
    ]).sudo().unlink()
