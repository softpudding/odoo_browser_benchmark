"""Cleanup for website_sale.publish_shop_product."""


def cleanup(env):
    env["product.template"].search([("name", "=", "Shop Special Chair")]).unlink()
