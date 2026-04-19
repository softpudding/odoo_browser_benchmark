"""Clean up artifacts from previous runs."""


def cleanup(env):
    partner = env["res.partner"].search(
        [("name", "=", "Bench Partial Co")], limit=1
    )

    # Unreconcile and delete payments for this partner first
    if partner:
        payments = env["account.payment"].search([
            ("partner_id", "=", partner.id),
        ])
        for pay in payments:
            move = pay.move_id
            if move:
                for line in move.line_ids.filtered(
                    lambda l: l.matched_debit_ids or l.matched_credit_ids
                ):
                    line.remove_move_reconcile()
            if pay.state == "posted":
                try:
                    pay.action_draft()
                except Exception:
                    pass
            try:
                pay.action_cancel()
            except Exception:
                pass
            try:
                pay.unlink()
            except Exception:
                if pay.move_id:
                    try:
                        pay.move_id.button_cancel()
                    except Exception:
                        pass

    # Delete the source invoices (target + distractor) and any reversals
    for ref in ("BENCH-PARTIAL-001", "BENCH-PARTIAL-DISTRACT"):
        moves = env["account.move"].search([("ref", "=", ref)])
        for move in moves:
            for line in move.line_ids.filtered(
                lambda l: l.matched_debit_ids or l.matched_credit_ids
            ):
                line.remove_move_reconcile()
            reversals = env["account.move"].search([
                ("reversed_entry_id", "=", move.id),
            ])
            for rev in reversals:
                if rev.state == "posted":
                    rev.button_draft()
                rev.button_cancel()
                rev.unlink()
            if move.state == "posted":
                move.button_draft()
            move.button_cancel()
            move.unlink()

    # Sweep any remaining customer invoices/refunds for this partner
    if partner:
        orphans = env["account.move"].search([
            ("partner_id", "=", partner.id),
            ("move_type", "in", ["out_invoice", "out_refund"]),
        ])
        for m in orphans:
            for line in m.line_ids.filtered(
                lambda l: l.matched_debit_ids or l.matched_credit_ids
            ):
                line.remove_move_reconcile()
            if m.state == "posted":
                m.button_draft()
            m.button_cancel()
            m.unlink()

        partner.unlink()

    # Remove the seeded secondary bank journal if it exists and is unused.
    secondary = env["account.journal"].search(
        [("name", "=", "Bench Secondary Bank")], limit=1
    )
    if secondary:
        # Only unlink if no journal items reference it.
        refs = env["account.move.line"].search_count(
            [("journal_id", "=", secondary.id)]
        )
        if refs == 0:
            try:
                secondary.unlink()
            except Exception:
                pass
