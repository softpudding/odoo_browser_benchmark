"""Cleanup for account.switch_negative_invoice_repair_credit_note."""


def cleanup(env):
    partner = env["res.partner"].search([("name", "=", "Lumen Works")], limit=1)
    if not partner:
        return

    moves = env["account.move"].search([
        ("partner_id", "=", partner.id),
        ("invoice_origin", "in", ["RET-507", "RET-508"]),
    ])
    posted = moves.filtered(lambda move: move.state == "posted")
    if posted:
        posted.button_draft()
    moves.unlink()
