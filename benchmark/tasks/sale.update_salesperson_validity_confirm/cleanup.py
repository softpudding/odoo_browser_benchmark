"""Cleanup for sale.update_salesperson_validity_confirm."""


def cleanup(env):
    orders = env["sale.order"].search([("name", "in", ["S-QUOTE-VAL-01", "S-QUOTE-VAL-02"])])
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
