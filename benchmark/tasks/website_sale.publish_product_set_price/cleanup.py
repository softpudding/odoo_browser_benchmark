"""Cleanup for website_sale.publish_product_set_price."""


def cleanup(env):
    env["product.template"].search([("name", "=", "Summit Standing Desk")]).unlink()
