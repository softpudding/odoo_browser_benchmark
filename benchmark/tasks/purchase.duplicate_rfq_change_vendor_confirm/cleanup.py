"""Clean up artifacts from previous runs."""


def cleanup(env):
    orders = env["purchase.order"].search([
        ("partner_ref", "in", ["BENCH-RFQ-DUP", "PH-REISSUE-77"]),
    ])
    for order in orders:
        if order.state in ("purchase", "done"):
            order.button_cancel()
        order.unlink()
