"""Cleanup for account.create_customer_invoice_post."""

INVOICE_REF = "NWA-AR-220"


def cleanup(env):
    moves = env["account.move"].search([
        ("move_type", "=", "out_invoice"),
        ("ref", "=", INVOICE_REF),
    ])
    for move in moves:
        for payment in move._get_reconciled_payments():
            if payment.state == "posted":
                payment.action_draft()
            payment.unlink()
        if move.state == "posted":
            move.button_draft()
        if move.state == "draft":
            move.button_cancel()
        move.unlink()
