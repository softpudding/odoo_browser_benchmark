"""Clean up artifacts from previous runs."""


def cleanup(env):
    partner = env["res.partner"].search([("name", "=", "Azure Interior")], limit=1)
    if not partner:
        return
    orders = env["sale.order"].search([
        ("partner_id", "=", partner.id),
        ("client_order_ref", "in", ["BENCH-PMT-01", "AZ-2026-Q2"]),
    ])
    for order in orders:
        if order.state == "sale":
            order.action_cancel()
        order.unlink()
