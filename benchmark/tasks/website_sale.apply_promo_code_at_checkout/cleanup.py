"""Cleanup for website_sale.apply_promo_code_at_checkout."""


PROGRAM_NAME = "Bench Promo 10%"
CUSTOMER_NAME = "Bench Promo Customer"
PRODUCT_NAME = "Bench Promo Product"
ORDER_REF = "SO-BENCH-001"


def cleanup(env):
    orders = env["sale.order"].with_context(active_test=False).search([
        ("client_order_ref", "=", ORDER_REF),
    ])
    if orders:
        orders.filtered(lambda o: o.state not in ("draft", "cancel")).sudo().action_cancel()
        orders.sudo().unlink()

    progs = env["loyalty.program"].with_context(active_test=False).search([
        ("name", "=", PROGRAM_NAME),
    ])
    if progs:
        env["loyalty.card"].with_context(active_test=False).search([
            ("program_id", "in", progs.ids),
        ]).sudo().unlink()
        progs.write({"active": False})
        progs.sudo().unlink()

    env["product.template"].with_context(active_test=False).search([
        ("name", "=", PRODUCT_NAME),
    ]).sudo().unlink()

    env["res.partner"].with_context(active_test=False).search([
        ("name", "=", CUSTOMER_NAME),
    ]).sudo().unlink()
