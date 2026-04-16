"""Cleanup for sale.set_commitment_date."""

PARTNER_NAME = "Highfield Consulting"
TARGET_REF = "BENCH-COMMIT-01"
DISTRACTOR_REF = "BENCH-COMMIT-02"


def cleanup(env):
    orders = env["sale.order"].search([
        ("client_order_ref", "in", [TARGET_REF, DISTRACTOR_REF])
    ])
    for order in orders:
        for inv in order.invoice_ids:
            if inv.state == "posted":
                inv.button_draft()
            inv.unlink()
        if order.state == "sale":
            order.action_cancel()
        if order.state == "cancel":
            order.action_draft()
        order.unlink()
