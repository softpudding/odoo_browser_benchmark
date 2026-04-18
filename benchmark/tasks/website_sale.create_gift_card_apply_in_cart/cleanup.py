"""Cleanup for website_sale.create_gift_card_apply_in_cart."""


PROGRAM_NAME = "Spring Gift Card"
PRODUCT_NAME = "Spring Premium Bundle"
ORDER_REF = "SPRING-GIFTCARD-CART-01"


def cleanup(env):
    env["sale.order"].with_context(active_test=False).search([
        ("client_order_ref", "=", ORDER_REF),
    ]).sudo().unlink()
    progs = env["loyalty.program"].with_context(active_test=False).search([
        ("name", "=", PROGRAM_NAME),
    ])
    if progs:
        env["loyalty.card"].with_context(active_test=False).search([
            ("program_id", "in", progs.ids),
        ]).sudo().unlink()
        progs.write({"active": False})
        progs.unlink()
    env["product.template"].with_context(active_test=False).search([
        ("name", "=", PRODUCT_NAME),
    ]).sudo().unlink()
