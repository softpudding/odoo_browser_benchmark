"""Clean up credit-note task artifacts from previous runs."""


def cleanup(env):
    partner = env["res.partner"].search([("name", "=", "Lumen Works")], limit=1)
    if not partner:
        return

    moves = env["account.move"].search([
        ("partner_id", "=", partner.id),
        ("move_type", "in", ["out_invoice", "out_refund"]),
    ])
    posted = moves.filtered(lambda move: move.state == "posted")
    if posted:
        posted.button_draft()
    moves.unlink()


