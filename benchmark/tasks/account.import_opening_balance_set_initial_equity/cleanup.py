"""Cleanup for account.import_opening_balance_set_initial_equity."""

REF = "OPEN-BAL-001"


def cleanup(env):
    moves = env["account.move"].search([
        ("move_type", "=", "entry"),
        ("ref", "=", REF),
    ])
    for mv in moves:
        if mv.state == "posted":
            try:
                mv.button_draft()
            except Exception:
                pass
        if mv.state != "cancel":
            try:
                mv.button_cancel()
            except Exception:
                pass
        try:
            mv.unlink()
        except Exception:
            pass
