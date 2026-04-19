"""Cleanup for sale_loyalty.buy_x_get_y_reward_in_cart."""


PROGRAM_NAME = "Bench BOGO"
CUSTOMER_NAME = "Bench Promo Customer"
PRODUCT_NAME = "Bench Promo Widget"


def cleanup(env):
    partner = env["res.partner"].with_context(active_test=False).search([
        ("name", "=", CUSTOMER_NAME),
    ], limit=1)
    if partner:
        orders = env["sale.order"].with_context(active_test=False).search([
            ("partner_id", "=", partner.id),
        ])
        if orders:
            confirmed = orders.filtered(lambda o: o.state not in ("draft", "cancel"))
            if confirmed:
                confirmed.sudo()._action_cancel()
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

    tmpl = env["product.template"].with_context(active_test=False).search([
        ("name", "=", PRODUCT_NAME),
    ])
    if tmpl:
        variant_ids = tmpl.product_variant_ids.ids
        if variant_ids:
            leftover_lines = env["sale.order.line"].with_context(active_test=False).search([
                ("product_id", "in", variant_ids),
            ])
            if leftover_lines:
                leftover_orders = leftover_lines.order_id
                if leftover_orders:
                    confirmed = leftover_orders.filtered(
                        lambda o: o.state not in ("draft", "cancel")
                    )
                    if confirmed:
                        confirmed.sudo()._action_cancel()
                    leftover_orders.sudo().unlink()
        tmpl.sudo().unlink()

    if partner:
        partner.sudo().unlink()
