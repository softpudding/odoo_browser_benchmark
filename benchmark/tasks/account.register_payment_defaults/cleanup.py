"""Clean up artifacts from previous runs."""


def cleanup(env):
    # Remove payments created by the task
    payments = env["account.payment"].search([("memo", "=", "BENCH-PAY-01")])
    for pmt in payments:
        if pmt.state == "posted":
            pmt.action_draft()
        pmt.unlink()

    # Reset invoice payment_state by unreconciling and re-posting
    invoice = env["account.move"].search([("ref", "=", "BENCH-PAY-01")])
    for mv in invoice:
        # Unreconcile any payment lines
        for line in mv.line_ids.filtered(
            lambda l: l.matched_debit_ids or l.matched_credit_ids
        ):
            line.remove_move_reconcile()
        # Re-trigger payment_state computation by re-posting
        if mv.state == "posted":
            mv.button_draft()
            mv.action_post()
