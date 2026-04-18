"""Cleanup for point_of_sale.add_item_apply_global_discount_pay_cash."""


CONFIG_NAME = "Bench Test Store"
PRODUCT_NAME = "Bench POS Widget"
CASH_METHOD = "Bench Cash"


def cleanup(env):
    env["pos.order"].search([("config_id.name", "=", CONFIG_NAME)]).unlink()
    env["pos.session"].search([("config_id.name", "=", CONFIG_NAME)]).unlink()
    env["pos.config"].search([("name", "=", CONFIG_NAME)]).unlink()
    env["pos.payment.method"].search([("name", "=", CASH_METHOD)]).unlink()
    env["product.template"].search([("name", "=", PRODUCT_NAME)]).unlink()
