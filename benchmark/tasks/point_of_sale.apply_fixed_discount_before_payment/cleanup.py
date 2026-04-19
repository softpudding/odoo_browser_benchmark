"""Cleanup for point_of_sale.apply_fixed_discount_before_payment."""


CONFIG_NAME = "Bench POS"
PRODUCT_A_NAME = "Bench POS Item A"
PRODUCT_B_NAME = "Bench POS Item B"
CASH_METHOD = "Bench Cash"


def cleanup(env):
    env["pos.order"].search([("config_id.name", "=", CONFIG_NAME)]).unlink()
    env["pos.session"].search([("config_id.name", "=", CONFIG_NAME)]).unlink()
    env["pos.config"].search([("name", "=", CONFIG_NAME)]).unlink()
    env["pos.payment.method"].search([("name", "=", CASH_METHOD)]).unlink()
    env["product.template"].search([
        ("name", "in", [PRODUCT_A_NAME, PRODUCT_B_NAME]),
    ]).unlink()
