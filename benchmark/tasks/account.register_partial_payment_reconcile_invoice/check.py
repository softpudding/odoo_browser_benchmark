"""Postcondition checks for account.register_partial_payment_reconcile_invoice."""


def check(env):
    failures = []

    invoice = env["account.move"].search(
        [("ref", "=", "BENCH-PARTIAL-001")], limit=1
    )
    if not invoice:
        return ["Source invoice BENCH-PARTIAL-001 not found"]

    distractor = env["account.move"].search(
        [("ref", "=", "BENCH-PARTIAL-DISTRACT")], limit=1
    )
    if not distractor:
        failures.append("Distractor invoice BENCH-PARTIAL-DISTRACT not found")

    # -- Target invoice: must remain posted, with payment_state == 'partial' --
    if invoice.move_type != "out_invoice":
        failures.append(
            f"BENCH-PARTIAL-001 move_type is {invoice.move_type!r}, expected 'out_invoice'"
        )
    if invoice.state != "posted":
        failures.append(
            f"BENCH-PARTIAL-001 state is {invoice.state!r}, expected 'posted' "
            f"(invoice must remain posted, not draft or cancelled)"
        )
    if invoice.payment_state != "partial":
        failures.append(
            f"BENCH-PARTIAL-001 payment_state is {invoice.payment_state!r}, "
            f"expected 'partial' (agent must register a PARTIAL 200.00 payment, "
            f"not a full 500.00 payment)"
        )
    if abs(invoice.amount_total - 500.0) > 0.01:
        failures.append(
            f"BENCH-PARTIAL-001 amount_total changed to {invoice.amount_total}, "
            f"expected 500.0 (invoice must be untouched)"
        )
    if abs(invoice.amount_residual - 300.0) > 0.01:
        failures.append(
            f"BENCH-PARTIAL-001 amount_residual is {invoice.amount_residual}, "
            f"expected 300.0 (500 total minus 200 paid)"
        )

    # -- Distractor invoice: must remain unpaid/untouched --
    if distractor:
        if distractor.state != "posted":
            failures.append(
                f"BENCH-PARTIAL-DISTRACT state is {distractor.state!r}, "
                f"expected 'posted' (must not be touched)"
            )
        if distractor.payment_state != "not_paid":
            failures.append(
                f"BENCH-PARTIAL-DISTRACT payment_state is "
                f"{distractor.payment_state!r}, expected 'not_paid' "
                f"(distractor invoice must remain unpaid)"
            )
        if abs(distractor.amount_total - 300.0) > 0.01:
            failures.append(
                f"BENCH-PARTIAL-DISTRACT amount_total changed to "
                f"{distractor.amount_total}, expected 300.0"
            )

    partner = env["res.partner"].search([("name", "=", "Bench Partial Co")], limit=1)
    if not partner:
        return failures + ["Partner 'Bench Partial Co' not found"]

    payments = env["account.payment"].search([
        ("partner_id", "=", partner.id),
    ])
    if not payments:
        failures.append("No account.payment found for Bench Partial Co")
        return failures
    if len(payments) != 1:
        failures.append(
            f"Expected exactly 1 account.payment for Bench Partial Co, "
            f"found {len(payments)}"
        )

    pay = payments[0]
    # With auto-reconcile on, a fully-reconciled payment reports state='paid';
    # a partial one may report 'posted' or 'in_process'. Accept all posted-ish.
    if pay.state not in ("posted", "paid", "in_process"):
        failures.append(
            f"Payment state is {pay.state!r}, expected 'posted', 'paid', "
            f"or 'in_process'"
        )
    if abs(pay.amount - 200.0) > 0.01:
        failures.append(
            f"Payment amount is {pay.amount}, expected 200.0 (agent must have "
            f"overridden the wizard default of 500.0)"
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
    expected_memo = "Partial 1 of 2 for BENCH-PARTIAL-001"
    if (pay.memo or "").strip() != expected_memo:
        failures.append(
            f"Payment memo is {pay.memo!r}, expected {expected_memo!r} "
            f"(agent must OVERRIDE the wizard's auto-filled invoice-name "
            f"memo with this exact string)"
        )
    # Back-dated payment date: 2026-04-15 (today is 2026-04-19 in the
    # benchmark environment).
    from datetime import date as _date
    expected_date = _date(2026, 4, 15)
    pay_date = pay.date
    if hasattr(pay_date, "date"):
        # Sometimes Odoo returns a datetime — normalise.
        pay_date = pay_date.date()
    if pay_date != expected_date:
        failures.append(
            f"Payment date is {pay.date!r}, expected {expected_date!s} "
            f"(agent must back-date the Payment Date from today's default)"
        )

    # Verify reconciliation between payment and the TARGET invoice.
    invoice_receivable_lines = invoice.line_ids.filtered(
        lambda l: l.account_id.account_type == "asset_receivable"
    )
    if not invoice_receivable_lines:
        failures.append("Invoice has no receivable lines (unexpected state)")
    else:
        reconciled = any(
            line.reconciled or line.matched_debit_ids or line.matched_credit_ids
            for line in invoice_receivable_lines
        )
        if not reconciled:
            failures.append(
                "BENCH-PARTIAL-001 receivable lines are not reconciled "
                "with the payment"
            )

    # The payment's journal entry should be posted.
    if pay.move_id and pay.move_id.state != "posted":
        failures.append(
            f"Payment journal entry state is {pay.move_id.state!r}, "
            f"expected 'posted'"
        )

    # The payment's journal must be the original Bank journal (not Cash
    # and not the distractor 'Bench Secondary Bank').
    if pay.journal_id and pay.journal_id.type != "bank":
        failures.append(
            f"Payment journal type is {pay.journal_id.type!r}, expected 'bank'"
        )
    if pay.journal_id and pay.journal_id.name != "Bank":
        failures.append(
            f"Payment journal name is {pay.journal_id.name!r}, expected "
            f"'Bank' (agent must OVERRIDE the wizard default 'Bench "
            f"Secondary Bank' with the original 'Bank' journal)"
        )

    # The distractor invoice's receivable line must NOT be reconciled.
    if distractor:
        distractor_receivable = distractor.line_ids.filtered(
            lambda l: l.account_id.account_type == "asset_receivable"
        )
        for line in distractor_receivable:
            if line.reconciled or line.matched_debit_ids or line.matched_credit_ids:
                failures.append(
                    "BENCH-PARTIAL-DISTRACT receivable line was reconciled — "
                    "agent registered payment against the WRONG invoice"
                )
                break

    return failures
