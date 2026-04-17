"""Clean up artifacts from previous runs."""


def cleanup(env):
    orders = env["purchase.order"].search([("origin", "in", ["MED-RFQ-NOTE-01", "MED-RFQ-NOTE-02"])])
    for order in orders:
        if order.state in ("purchase", "done"):
            order.button_cancel()
        order.unlink()
