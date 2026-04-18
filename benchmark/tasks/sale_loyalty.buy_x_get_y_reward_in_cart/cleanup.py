"""Cleanup for sale_loyalty.buy_x_get_y_reward_in_cart."""


PROGRAM_NAME = "Buy 2 Widgets Get 1 Gadget"
DISTRACTOR_NAME = "Winter Bundle 3%"
BUY_PRODUCT_NAME = "Bench Widget"
REWARD_PRODUCT_NAME = "Bench Gadget"
ORDER_REF = "BXGY-WIDGET-CART-01"


def cleanup(env):
    env["sale.order"].with_context(active_test=False).search([
        ("client_order_ref", "=", ORDER_REF),
    ]).sudo().unlink()
    progs = env["loyalty.program"].with_context(active_test=False).search([
        ("name", "in", [PROGRAM_NAME, DISTRACTOR_NAME]),
    ])
    if progs:
        progs.write({"active": False})
        progs.unlink()
    env["product.template"].with_context(active_test=False).search([
        ("name", "in", [BUY_PRODUCT_NAME, REWARD_PRODUCT_NAME]),
    ]).sudo().unlink()
