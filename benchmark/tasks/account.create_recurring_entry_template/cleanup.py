"""Cleanup for account.create_recurring_entry_template."""

REF = "Bench Office Supplies Tmpl"


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
