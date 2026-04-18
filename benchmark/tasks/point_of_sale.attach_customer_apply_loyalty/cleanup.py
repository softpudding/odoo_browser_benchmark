"""Cleanup for point_of_sale.attach_customer_apply_loyalty."""


CONFIG_NAME = "Bench Loyalty POS"
PRODUCT_NAME = "Bench POS Item"
CASH_METHOD = "Bench Loyalty Cash"
PROGRAM_NAME = "Bench Loyalty Program"
PARTNER_NAME = "Loyal Larry"


def cleanup(env):
    env["pos.order"].search([("config_id.name", "=", CONFIG_NAME)]).unlink()
    env["pos.session"].search([("config_id.name", "=", CONFIG_NAME)]).unlink()
    env["pos.config"].search([("name", "=", CONFIG_NAME)]).unlink()
    env["pos.payment.method"].search([("name", "=", CASH_METHOD)]).unlink()
    env["product.template"].search([("name", "=", PRODUCT_NAME)]).unlink()

    progs = env["loyalty.program"].with_context(active_test=False).search([
        ("name", "=", PROGRAM_NAME),
    ])
    cards = env["loyalty.card"].with_context(active_test=False).search([
        ("program_id", "in", progs.ids),
    ])
    cards.unlink()
    if progs:
        progs.write({"active": False})
        progs.unlink()

    env["res.partner"].search([("name", "=", PARTNER_NAME)]).unlink()
