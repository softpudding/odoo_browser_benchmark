"""Clean up artifacts created by seed.py or the agent run."""

PARTNER_NAME = "Bench Add Co"
SO_NAME = "BENCH-ADD-LINE"
PRODUCT_EXISTING = "Bench Existing Item"
PRODUCT_EXTRA = "Bench Extra Item"


def cleanup(env):
    partner = env["res.partner"].with_context(active_test=False).search(
        [("name", "=", PARTNER_NAME)], limit=1
    )
    if partner:
        orders = env["sale.order"].with_context(active_test=False).search([
            ("partner_id", "=", partner.id),
        ])
        for order in orders:
            if order.state == "sale":
                try:
                    order.action_cancel()
                except Exception:
                    pass
            order.sudo().unlink()

    # Sweep anything still carrying the source name
    stragglers = env["sale.order"].with_context(active_test=False).search(
        [("name", "=", SO_NAME)]
    )
    for order in stragglers:
        if order.state == "sale":
            try:
                order.action_cancel()
            except Exception:
                pass
        order.sudo().unlink()

    if partner:
        partner.sudo().unlink()

    for pname in (PRODUCT_EXISTING, PRODUCT_EXTRA):
        product = env["product.product"].with_context(active_test=False).search(
            [("name", "=", pname)]
        )
        if product:
            product.mapped("product_tmpl_id").sudo().unlink()
