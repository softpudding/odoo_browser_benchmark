"""Clean up artifacts created by seed.py or the agent run."""

PARTNER_NAME = "Bench Cancel Co"
CLIENT_REF = "BENCH-CANCEL-RESTORE"
PRODUCT_A = "Bench Cancel Item A"
PRODUCT_B = "Bench Cancel Item B"


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
            try:
                order.sudo().unlink()
            except Exception:
                pass

    # Sweep any SO bearing the client_order_ref
    stragglers = env["sale.order"].with_context(active_test=False).search(
        [("client_order_ref", "=", CLIENT_REF)]
    )
    for order in stragglers:
        if order.state == "sale":
            try:
                order.action_cancel()
            except Exception:
                pass
        try:
            order.sudo().unlink()
        except Exception:
            pass

    if partner:
        partner.sudo().unlink()

    for pname in (PRODUCT_A, PRODUCT_B):
        product = env["product.product"].with_context(active_test=False).search(
            [("name", "=", pname)]
        )
        if product:
            product.mapped("product_tmpl_id").sudo().unlink()
