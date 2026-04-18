"""Cleanup for account.create_recurring_journal_entry."""

REF = "Bench Rent Apr"


def cleanup(env):
    moves = env["account.move"].search([
        ("move_type", "=", "entry"),
        ("ref", "=", REF),
    ])
    for mv in moves:
        if mv.state == "posted":
            mv.button_draft()
        if mv.state != "cancel":
            try:
                mv.button_cancel()
            except Exception:
                pass
        mv.unlink()

    leftover = env["mail.activity"].search([
        ("summary", "=", "Post next month's rent entry"),
        ("res_model", "=", "account.move"),
    ])
    leftover.unlink()
