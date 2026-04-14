"""Clean up partner and invoice artifacts from previous runs."""


def cleanup(env):
    partners = env["res.partner"].search([
        ("name", "in", ["Northwind Studio East", "Northwind Studio West"]),
    ])
    moves = env["account.move"].search([
        ("partner_id", "in", partners.ids),
        ("move_type", "=", "out_invoice"),
    ])
    posted = moves.filtered(lambda move: move.state == "posted")
    if posted:
        posted.button_draft()
    moves.unlink()
    partners.unlink()


