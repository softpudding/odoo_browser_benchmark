"""Cleanup for point_of_sale.refund_previous_order."""


CONFIG_NAME = "Bench Refund POS"
PRODUCT_NAME = "Bench Widget"
CASH_METHOD = "Bench Refund Cash"
CASH_JOURNAL = "Bench Refund Cash Journal"


def cleanup(env):
    env["pos.order"].search([("config_id.name", "=", CONFIG_NAME)]).unlink()
    env["pos.session"].search([("config_id.name", "=", CONFIG_NAME)]).unlink()
    env["pos.config"].search([("name", "=", CONFIG_NAME)]).unlink()
    env["pos.payment.method"].search([("name", "=", CASH_METHOD)]).unlink()
    env["account.journal"].search([("name", "=", CASH_JOURNAL)]).unlink()
    env["product.template"].search([("name", "=", PRODUCT_NAME)]).unlink()
