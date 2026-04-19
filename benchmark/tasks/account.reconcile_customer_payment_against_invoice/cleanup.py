"""Clean up artifacts from previous runs."""


def cleanup(env):
    partner = env["res.partner"].search([("name", "=", "Bench Recon Co")], limit=1)

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
                # If unlink fails, ensure the underlying move is cancelled and deleted
                if pay.move_id:
                    try:
                        pay.move_id.button_cancel()
                    except Exception:
                        pass

    # Now delete the source invoice and any reversals linked to it
    moves = env["account.move"].search([("ref", "=", "INV/BENCH/RECON")])
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
