"""Postcondition checks for account.reconcile_customer_payment_against_invoice."""


def check(env):
    failures = []

    invoice = env["account.move"].search([("ref", "=", "INV/BENCH/RECON")], limit=1)
    if not invoice:
        return ["Source invoice INV/BENCH/RECON not found"]

    if invoice.move_type != "out_invoice":
        failures.append(
            f"INV/BENCH/RECON move_type is {invoice.move_type!r}, expected 'out_invoice'"
        )
    if invoice.state != "posted":
        failures.append(
            f"INV/BENCH/RECON state is {invoice.state!r}, expected 'posted' "
            f"(invoice must remain posted, not draft or cancelled)"
        )
    if invoice.payment_state not in ("paid", "in_payment"):
        failures.append(
            f"INV/BENCH/RECON payment_state is {invoice.payment_state!r}, "
            f"expected 'paid' or 'in_payment' (payment must be registered and "
            f"reconciled)"
        )
    if abs(invoice.amount_total - 500.0) > 0.01:
        failures.append(
            f"INV/BENCH/RECON amount_total changed to {invoice.amount_total}, "
            f"expected 500.0 (invoice must be untouched)"
        )

    partner = env["res.partner"].search([("name", "=", "Bench Recon Co")], limit=1)
    if not partner:
        return failures + ["Partner 'Bench Recon Co' not found"]

    payments = env["account.payment"].search([
        ("partner_id", "=", partner.id),
    ])
    if not payments:
        failures.append(
            "No account.payment found for Bench Recon Co"
        )
        return failures
    if len(payments) != 1:
        failures.append(
            f"Expected exactly 1 account.payment for Bench Recon Co, "
            f"found {len(payments)}"
        )

    pay = payments[0]
    # On Odoo 19 with auto-reconcile, a posted account.payment whose
    # receivable line has been fully reconciled reports state='paid'
    # (reconciled). Both 'posted' and 'paid' mean the payment was posted.
    if pay.state not in ("posted", "paid", "in_process"):
        failures.append(
            f"Payment state is {pay.state!r}, expected 'posted', 'paid', or 'in_process'"
        )
    if abs(pay.amount - 500.0) > 0.01:
        failures.append(
            f"Payment amount is {pay.amount}, expected 500.0"
        )
    if pay.payment_type != "inbound":
        failures.append(
            f"Payment payment_type is {pay.payment_type!r}, expected 'inbound' "
            f"(inbound = customer payment)"
        )
    if pay.partner_id.id != partner.id:
        failures.append(
            f"Payment partner_id is {pay.partner_id.name!r}, expected "
            f"{partner.name!r}"
        )

    # Verify reconciliation between payment and invoice
    invoice_receivable_lines = invoice.line_ids.filtered(
        lambda l: l.account_id.account_type == "asset_receivable"
    )
    if not invoice_receivable_lines:
        failures.append(
            "Invoice has no receivable lines (unexpected state)"
        )
    else:
        reconciled = any(
            line.reconciled or line.matched_debit_ids or line.matched_credit_ids
            for line in invoice_receivable_lines
        )
        if not reconciled:
            failures.append(
                "Invoice receivable lines are not reconciled with any payment"
            )

    # The payment's journal entry should reference the partner
    if pay.move_id and pay.move_id.state != "posted":
        failures.append(
            f"Payment journal entry state is {pay.move_id.state!r}, expected 'posted'"
        )

    # Ensure the payment's journal is a Bank journal (not Cash)
    if pay.journal_id and pay.journal_id.type != "bank":
        failures.append(
            f"Payment journal type is {pay.journal_id.type!r}, expected 'bank'"
        )

    return failures
