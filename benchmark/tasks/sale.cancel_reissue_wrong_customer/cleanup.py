"""Clean up artifacts from previous runs."""


def cleanup(env):
    orders = env["sale.order"].search([
        ("client_order_ref", "in", ["SALE-FIX-12", "SALE-FIX-12-WEST"]),
    ])
    for order in orders:
        if order.state == "sale":
            order.action_cancel()
        if order.state in ("draft", "cancel"):
            order.unlink()
