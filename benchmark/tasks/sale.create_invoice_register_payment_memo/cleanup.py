"""Cleanup for sale.create_invoice_register_payment_memo."""


def cleanup(env):
    orders = env["sale.order"].search([
        ("client_order_ref", "in", ["PAYFLOW-01", "PAYFLOW-02"]),
    ])
    for order in orders:
        for invoice in order.invoice_ids.filtered(
            lambda move: move.move_type == "out_invoice"
        ):
            for payment in invoice._get_reconciled_payments():
                if payment.state == "posted":
                    payment.action_draft()
                payment.unlink()
            if invoice.state == "posted":
                invoice.button_draft()
            invoice.unlink()
        if order.state == "sale":
            order.action_cancel()
        order.unlink()
