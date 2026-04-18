"""Clean up artifacts from previous runs."""

ORDER_REF = "S-BENCH-OPT-001"


def cleanup(env):
    orders = env["sale.order"].with_context(active_test=False).search([
        ("client_order_ref", "=", ORDER_REF),
    ])
    for order in orders:
        if order.state not in ("draft", "cancel"):
            try:
                order.action_cancel()
            except Exception:
                pass
        order.unlink()
