"""Cleanup for account.reconcile_bank_statement_line_manual.

Reverses the seed: unreconciles, unlinks bank statement line and invoice.
"""

PARTNER_NAME = "Bench Reconcile Customer"
PAYMENT_REF = "Bench Reconcile 500"


def cleanup(env):
    # Unreconcile + delete seeded bank statement line(s)
    stl_model = env["account.bank.statement.line"]
    stls = stl_model.search([("payment_ref", "=", PAYMENT_REF)])
    for stl in stls:
        try:
            stl.action_undo_reconciliation()
        except Exception:
            pass
        mv = stl.move_id
        try:
            if stl.statement_id:
                stl.statement_id = False
        except Exception:
            pass
        if mv and mv.state == "posted":
            try:
                mv.button_draft()
            except Exception:
                pass
        try:
            stl.unlink()
        except Exception:
            pass
        if mv and mv.exists():
            try:
                if mv.state != "cancel":
                    mv.button_cancel()
            except Exception:
                pass
            try:
                mv.unlink()
            except Exception:
                pass

    # Delete customer invoices for the seeded partner
    partner = env["res.partner"].search([("name", "=", PARTNER_NAME)], limit=1)
    if partner:
        invs = env["account.move"].search([
            ("partner_id", "=", partner.id),
            ("move_type", "=", "out_invoice"),
        ])
        for inv in invs:
            for line in inv.line_ids.filtered(
                lambda l: l.matched_debit_ids or l.matched_credit_ids
            ):
                try:
                    line.remove_move_reconcile()
                except Exception:
                    pass
            if inv.state == "posted":
                try:
                    inv.button_draft()
                except Exception:
                    pass
            try:
                inv.button_cancel()
            except Exception:
                pass
            try:
                inv.unlink()
            except Exception:
                pass
