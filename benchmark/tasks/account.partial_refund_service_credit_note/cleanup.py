"""Clean up artifacts from previous runs."""


def cleanup(env):
    for ref in ["CN-SERVICE-01", "CN-SERVICE-02"]:
        moves = env["account.move"].search([("ref", "=", ref)])
        for move in moves:
            reversals = env["account.move"].search([
                ("reversed_entry_id", "=", move.id),
            ])
            for reversal in reversals:
                if reversal.state == "posted":
                    reversal.button_draft()
                reversal.button_cancel()
                reversal.unlink()
            for line in move.line_ids.filtered(
                lambda l: l.matched_debit_ids or l.matched_credit_ids
            ):
                line.remove_move_reconcile()
            if move.state == "posted":
                move.button_draft()
            move.button_cancel()
            move.unlink()
