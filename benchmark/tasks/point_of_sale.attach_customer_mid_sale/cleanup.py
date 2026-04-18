"""Cleanup for point_of_sale.attach_customer_mid_sale."""


CONFIG_NAME = "Bench Easy POS"
PRODUCT_NAME = "Bench Easy POS Item"
CASH_METHOD = "Bench Easy Cash"
PARTNER_NAME = "Bench POS Easy Customer"


def cleanup(env):
    env["pos.order"].search([("config_id.name", "=", CONFIG_NAME)]).unlink()
    env["pos.session"].search([("config_id.name", "=", CONFIG_NAME)]).unlink()
    env["pos.config"].search([("name", "=", CONFIG_NAME)]).unlink()
    env["pos.payment.method"].search([("name", "=", CASH_METHOD)]).unlink()
    env["product.template"].search([("name", "=", PRODUCT_NAME)]).unlink()
    env["res.partner"].search([("name", "=", PARTNER_NAME)]).unlink()
