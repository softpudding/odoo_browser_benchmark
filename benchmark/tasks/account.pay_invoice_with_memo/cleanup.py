"""Cleanup for account.pay_invoice_with_memo."""

PARTNER_NAME = "Highfield Consulting"
TARGET_REF = "BENCH-PAYMEMO-01"
DISTRACTOR_REF = "BENCH-PAYMEMO-02"


def cleanup(env):
    partner = env["res.partner"].search([("name", "=", PARTNER_NAME)], limit=1)
    if not partner:
        return

    moves = env["account.move"].search([
        ("partner_id", "=", partner.id),
        ("ref", "in", [TARGET_REF, DISTRACTOR_REF]),
        ("move_type", "=", "out_invoice"),
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
