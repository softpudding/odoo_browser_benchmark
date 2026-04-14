"""Clean up artifacts from previous runs."""


def cleanup(env):
    partner = env["res.partner"].search([("name", "=", "Beacon Design")], limit=1)
    if partner:
        moves = env["account.move"].search([
            ("partner_id", "=", partner.id),
            ("move_type", "=", "out_invoice"),
        ])
        draft_moves = moves.filtered(lambda m: m.state == "draft")
        if draft_moves:
            draft_moves.unlink()
        posted_moves = moves.filtered(lambda m: m.state == "posted")
        if posted_moves:
            posted_moves.button_draft()
            posted_moves.unlink()


