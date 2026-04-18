"""Cleanup for point_of_sale.sell_two_products_apply_discount."""


CONFIG_NAME = "Bench Discount POS"
PRODUCT_PEN = "Bench POS Pen"
PRODUCT_NOTEBOOK = "Bench POS Notebook"
CASH_METHOD = "Bench Discount Cash"


def cleanup(env):
    env["pos.order"].search([("config_id.name", "=", CONFIG_NAME)]).unlink()
    env["pos.session"].search([("config_id.name", "=", CONFIG_NAME)]).unlink()
    env["pos.config"].search([("name", "=", CONFIG_NAME)]).unlink()
    env["pos.payment.method"].search([("name", "=", CASH_METHOD)]).unlink()
    env["product.template"].search([
        ("name", "in", [PRODUCT_PEN, PRODUCT_NOTEBOOK]),
    ]).unlink()
