"""Clean up artifacts from previous runs."""


def cleanup(env):
    orders = env["sale.order"].search([("client_order_ref", "=", "BENCH-PMT-02")])
    for order in orders:
        if order.state == "sale":
            order.action_cancel()
        order.unlink()
