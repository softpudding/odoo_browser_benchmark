"""Clean up artifacts created by seed.py or the agent run."""

PARTNER_NAME = "Bench Copy Co"
SOURCE_SO_NAME = "S-BENCH-COPY-001"
PRODUCT_A = "Bench SO Item A"
PRODUCT_B = "Bench SO Item B"


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

    # Sweep anything that still carries the source name too
    stragglers = env["sale.order"].with_context(active_test=False).search(
        [("name", "=", SOURCE_SO_NAME)]
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

    for pname in (PRODUCT_A, PRODUCT_B):
        product = env["product.product"].with_context(active_test=False).search(
            [("name", "=", pname)]
        )
        if product:
            product.mapped("product_tmpl_id").sudo().unlink()
