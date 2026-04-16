"""Clean up artifacts from previous runs."""


def cleanup(env):
    env["mail.activity"].search([("summary", "=", "Confirm dock appointment")]).unlink()

    orders = env["purchase.order"].search([
        ("partner_ref", "in", ["MED-RFQ-ACT-01", "MED-RFQ-ACT-02"]),
    ])
    for order in orders:
        if order.state in ("purchase", "done"):
            order.button_cancel()
        order.unlink()
