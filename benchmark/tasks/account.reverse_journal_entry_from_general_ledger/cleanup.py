"""Clean up artifacts from previous runs of the reversal-from-GL task."""


def cleanup(env):
    moves = env["account.move"].search([("ref", "=", "BENCH-GL-REV")])
    for move in moves:
        reversals = env["account.move"].search([
            ("reversed_entry_id", "=", move.id),
        ])
        for rev in reversals:
            if rev.state == "posted":
                try:
                    rev.button_draft()
                except Exception:
                    pass
            try:
                rev.button_cancel()
            except Exception:
                pass
            try:
                rev.unlink()
            except Exception:
                pass
        for line in move.line_ids.filtered(
            lambda l: l.matched_debit_ids or l.matched_credit_ids
        ):
            try:
                line.remove_move_reconcile()
            except Exception:
                pass
        if move.state == "posted":
            try:
                move.button_draft()
            except Exception:
                pass
        try:
            move.button_cancel()
        except Exception:
            pass
        try:
            move.unlink()
        except Exception:
            pass
