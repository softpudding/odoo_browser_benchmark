"""Clean up artifacts from previous runs."""

ORDER_REF = "BENCH-DISC-01"


def cleanup(env):
    orders = env["sale.order"].search([("client_order_ref", "=", ORDER_REF)])
    for order in orders:
        if order.state != "draft":
            order.action_cancel()
        order.unlink()