"""Clean up artifacts from previous runs."""


def cleanup(env):
    orders = env["sale.order"].search([
        ("client_order_ref", "in", ["MED-INV-SO-01", "MED-INV-SO-02"]),
    ])
    for order in orders:
        for invoice in order.invoice_ids.filtered(
            lambda move: move.move_type == "out_invoice"
        ):
            if invoice.state == "posted":
                invoice.button_draft()
            invoice.unlink()
        if order.state == "sale":
            order.action_cancel()
        order.unlink()
