"""Clean up artifacts from previous runs."""


def cleanup(env):
    partner = env["res.partner"].search([("name", "=", "Bench AR Co")], limit=1)

    moves = env["account.move"].search([("ref", "=", "INV/BENCH/001")])
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

    # Sweep out_refund drafts/posts still attached to the partner
    if partner:
        refunds = env["account.move"].search([
            ("move_type", "=", "out_refund"),
            ("partner_id", "=", partner.id),
        ])
        for ref in refunds:
            if ref.state == "posted":
                ref.button_draft()
            ref.button_cancel()
            ref.unlink()
        partner.unlink()
