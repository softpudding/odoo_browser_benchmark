"""Clean up artifacts created by seed.py or the agent run."""

PARTNER_ORIG = "Bench Orig Co"
PARTNER_CLONE = "Bench Clone Co"
CLIENT_REF = "BENCH-DUP"
PRODUCT_A = "Bench SO Dup Item A"
PRODUCT_B = "Bench SO Dup Item B"


def cleanup(env):
    # Sweep any SO bearing our client_order_ref
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

    # Sweep all SOs tied to either partner
    for pname in (PARTNER_ORIG, PARTNER_CLONE):
        partner = env["res.partner"].with_context(active_test=False).search(
            [("name", "=", pname)], limit=1
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
            try:
                partner.sudo().unlink()
            except Exception:
                pass

    for pname in (PRODUCT_A, PRODUCT_B):
        product = env["product.product"].with_context(active_test=False).search(
            [("name", "=", pname)]
        )
        if product:
            try:
                product.mapped("product_tmpl_id").sudo().unlink()
            except Exception:
                pass
