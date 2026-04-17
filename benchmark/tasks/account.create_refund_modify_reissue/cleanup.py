"""Clean up artifacts from previous runs of account.create_refund_modify_reissue."""


def cleanup(env):
    for ref in ["HLE-MOD-01", "HLS-DIST-01"]:
        moves = env["account.move"].search([("ref", "=", ref)])
        for mv in moves:
            # Clean reversals
            reversals = env["account.move"].search([
                ("reversed_entry_id", "=", mv.id),
            ])
            for rev in reversals:
                if rev.state == "posted":
                    rev.button_draft()
                rev.button_cancel()
                rev.unlink()
            # Unreconcile
            for line in mv.line_ids.filtered(
                lambda l: l.matched_debit_ids or l.matched_credit_ids
            ):
                line.remove_move_reconcile()
            if mv.state == "posted":
                mv.button_draft()
            mv.button_cancel()
            mv.unlink()

    # Clean up new draft invoices created by modify_moves
    for partner_name in ["Harborlight Engineering", "Harborlight Solutions"]:
        partner = env["res.partner"].search([("name", "=", partner_name)], limit=1)
        if partner:
            stale = env["account.move"].search([
                ("partner_id", "=", partner.id),
                ("move_type", "=", "out_invoice"),
                ("ref", "not in", ["HLE-MOD-01", "HLS-DIST-01"]),
            ])
            for s in stale:
                if s.state == "posted":
                    s.button_draft()
                s.button_cancel()
                s.unlink()
