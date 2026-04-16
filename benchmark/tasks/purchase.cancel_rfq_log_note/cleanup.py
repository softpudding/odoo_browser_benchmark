"""Cleanup for purchase.cancel_rfq_log_note."""


def cleanup(env):
    orders = env["purchase.order"].search([("name", "in", ["P-RFQ-CANCEL-01", "P-RFQ-CANCEL-02"])])
    if orders:
        env["mail.message"].search([
            ("model", "=", "purchase.order"),
            ("res_id", "in", orders.ids),
        ]).unlink()
        for order in orders:
            if order.state in ("purchase", "done"):
                order.button_cancel()
            order.unlink()
