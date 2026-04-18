"""Cleanup for point_of_sale.sell_pos_order_invoice_customer."""


CONFIG_NAME = "Bench Invoice POS"
PRODUCT_NAME = "Bench Invoice Item"
CASH_METHOD = "Bench Invoice Cash"
PARTNER_NAME = "Invoice Iris"


def cleanup(env):
    pos_orders = env["pos.order"].search([("config_id.name", "=", CONFIG_NAME)])
    moves = pos_orders.mapped("account_move")
    for mv in moves:
        if mv.state == "posted":
            try:
                mv.button_draft()
            except Exception:
                pass
        try:
            mv.unlink()
        except Exception:
            pass
    pos_orders.unlink()
    env["pos.session"].search([("config_id.name", "=", CONFIG_NAME)]).unlink()
    env["pos.config"].search([("name", "=", CONFIG_NAME)]).unlink()
    env["pos.payment.method"].search([("name", "=", CASH_METHOD)]).unlink()
    env["product.template"].search([("name", "=", PRODUCT_NAME)]).unlink()
    env["res.partner"].search([("name", "=", PARTNER_NAME)]).unlink()
