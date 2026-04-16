"""Clean up artifacts from previous runs."""


def cleanup(env):
    orders = env["sale.order"].search([
        ("client_order_ref", "in", ["BENCH-DUP-01", "SV-DUP-2026"]),
    ])
    for order in orders:
        if order.state == "sale":
            order.action_cancel()
        order.unlink()
