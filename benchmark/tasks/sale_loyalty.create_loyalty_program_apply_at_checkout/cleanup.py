"""Cleanup for sale_loyalty.create_loyalty_program_apply_at_checkout."""


PROGRAM_NAME = "Spring 10% Discount"
DISTRACTOR_NAME = "Holiday Bonus 5%"
PRODUCT_NAMES = ["Spring Lawn Chair", "Spring Garden Light"]
ORDER_REF = "SPRING-LOYAL-CART-01"


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
        ("name", "in", PRODUCT_NAMES),
    ]).sudo().unlink()
