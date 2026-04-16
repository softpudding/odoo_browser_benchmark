"""Clean up artifacts from previous runs."""


def cleanup(env):
    orders = env["purchase.order"].search([
        "|",
        ("partner_ref", "in", ["MED-RFQ-REF-01", "MED-RFQ-REF-02", "NCC-8842"]),
        ("origin", "in", ["MED-RFQ-REF-01", "MED-RFQ-REF-02"]),
    ])
    for order in orders:
        if order.state in ("purchase", "done"):
            order.button_cancel()
        order.unlink()
