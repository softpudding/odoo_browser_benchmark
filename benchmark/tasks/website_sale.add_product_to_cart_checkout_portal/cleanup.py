"""Cleanup for website_sale.add_product_to_cart_checkout_portal."""


PRODUCT_NAME = "Bench Portal Product"
CUSTOMER_NAME = "Bench Portal Customer"


def cleanup(env):
    partners = env["res.partner"].with_context(active_test=False).search([
        ("name", "=", CUSTOMER_NAME),
    ])
    if partners:
        orders = env["sale.order"].with_context(active_test=False).search([
            ("partner_id", "in", partners.ids),
        ])
        if orders:
            live = orders.filtered(lambda o: o.state not in ("draft", "cancel"))
            if live:
                live.sudo().action_cancel()
            orders.sudo().unlink()
        partners.sudo().unlink()

    tmpls = env["product.template"].with_context(active_test=False).search([
        ("name", "=", PRODUCT_NAME),
    ])
    if tmpls:
        variant_ids = tmpls.mapped("product_variant_ids").ids
        if variant_ids:
            leftover = env["sale.order"].with_context(active_test=False).search([
                ("order_line.product_id", "in", variant_ids),
            ])
            if leftover:
                live = leftover.filtered(lambda o: o.state not in ("draft", "cancel"))
                if live:
                    live.sudo().action_cancel()
                leftover.sudo().unlink()
        tmpls.sudo().unlink()
