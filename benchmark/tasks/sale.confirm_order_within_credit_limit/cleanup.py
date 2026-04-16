"""Clean up artifacts from previous runs."""


ORDER_REFS = ["CREDIT-OPS-07", "CREDIT-OPS-08", "CREDIT-OPS-09"]
INVOICE_REF = "CREDIT-LIMIT-OPEN-09"
CONTACT_NAMES = ["Atlas Credit Desk", "Atlas Fleet Credit Desk"]


def cleanup(env):
    env["res.partner"].search([("name", "in", CONTACT_NAMES)]).unlink()

    orders = env["sale.order"].search([("client_order_ref", "in", ORDER_REFS)])
    for order in orders:
        if order.state == "sale":
            order.action_cancel()
        if order.state in ("draft", "cancel"):
            order.unlink()

    moves = env["account.move"].search([("ref", "=", INVOICE_REF)])
    for mv in moves:
        for line in mv.line_ids.filtered(
            lambda l: l.matched_debit_ids or l.matched_credit_ids
        ):
            line.remove_move_reconcile()
        if mv.state == "posted":
            mv.button_draft()
        mv.button_cancel()
        mv.unlink()
