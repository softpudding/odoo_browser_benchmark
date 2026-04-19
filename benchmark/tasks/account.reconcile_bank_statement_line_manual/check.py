"""Postcondition checks for account.reconcile_bank_statement_line_manual.

Validates:
1. The bank statement line 'Bench Reconcile 500' exists, is fully
   reconciled (is_reconciled=True, amount_residual=0.0).
2. The customer invoice for Bench Reconcile Customer is posted, fully paid
   (payment_state='paid', amount_residual=0.0), unchanged in total (€500).
3. No extra invoice/statement-line was created.
4. The reconciliation actually links the statement-line move to the
   invoice's receivable line (i.e. the invoice's receivable line is
   reconciled).
"""

PARTNER_NAME = "Bench Reconcile Customer"
PAYMENT_REF = "Bench Reconcile 500"
INVOICE_AMOUNT = 500.00


def check(env):
    failures = []

    partner = env["res.partner"].search([("name", "=", PARTNER_NAME)], limit=1)
    if not partner:
        return [f"Partner {PARTNER_NAME!r} not found"]

    invoices = env["account.move"].search([
        ("partner_id", "=", partner.id),
        ("move_type", "=", "out_invoice"),
    ])
    if len(invoices) != 1:
        return [
            f"Expected exactly 1 customer invoice for {PARTNER_NAME!r}, "
            f"found {len(invoices)}"
        ]
    invoice = invoices[0]

    if invoice.state != "posted":
        failures.append(
            f"Invoice state is {invoice.state!r}, expected 'posted'"
        )

    if abs(invoice.amount_total - INVOICE_AMOUNT) > 0.01:
        failures.append(
            f"Invoice amount_total is {invoice.amount_total}, "
            f"expected {INVOICE_AMOUNT}"
        )

    if abs(invoice.amount_residual) > 0.01:
        failures.append(
            f"Invoice amount_residual is {invoice.amount_residual}, "
            f"expected 0.00 (invoice must be fully paid)"
        )

    if invoice.payment_state != "paid":
        failures.append(
            f"Invoice payment_state is {invoice.payment_state!r}, "
            f"expected 'paid'"
        )

    stls = env["account.bank.statement.line"].search([
        ("payment_ref", "=", PAYMENT_REF),
    ])
    if len(stls) != 1:
        failures.append(
            f"Expected exactly 1 bank statement line with payment_ref "
            f"{PAYMENT_REF!r}, found {len(stls)}"
        )
        return failures
    stl = stls[0]

    if stl.partner_id != partner:
        failures.append(
            f"Bank statement line partner is {stl.partner_id.name!r}, "
            f"expected {PARTNER_NAME!r}"
        )

    if abs(stl.amount - INVOICE_AMOUNT) > 0.01:
        failures.append(
            f"Bank statement line amount is {stl.amount}, "
            f"expected {INVOICE_AMOUNT}"
        )

    if not stl.is_reconciled:
        failures.append(
            f"Bank statement line is_reconciled is False, "
            f"expected True (fully reconciled)"
        )

    if abs(stl.amount_residual) > 0.01:
        failures.append(
            f"Bank statement line amount_residual is {stl.amount_residual}, "
            f"expected 0.00"
        )

    # Verify the invoice's receivable line is actually reconciled against
    # the statement line's move (not a distinct payment).
    recv_lines = invoice.line_ids.filtered(
        lambda l: l.account_id.account_type == "asset_receivable"
    )
    if len(recv_lines) != 1:
        failures.append(
            f"Expected 1 receivable line on invoice, found {len(recv_lines)}"
        )
    else:
        r = recv_lines[0]
        if not r.reconciled:
            failures.append(
                "Invoice's receivable line is not reconciled"
            )
        matched_moves = (
            r.matched_debit_ids.debit_move_id.move_id
            | r.matched_credit_ids.credit_move_id.move_id
        )
        if stl.move_id and stl.move_id not in matched_moves:
            failures.append(
                "Invoice receivable line is not reconciled against the "
                "bank statement line's move (might have been paid via a "
                "separate payment instead of by matching the statement)."
            )

    return failures
