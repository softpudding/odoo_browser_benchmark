"""Postcondition checks for account.pay_invoice_with_memo."""

from datetime import date


PARTNER_NAME = "Highfield Consulting"
TARGET_REF = "BENCH-PAYMEMO-01"
DISTRACTOR_REF = "BENCH-PAYMEMO-02"
EXPECTED_MEMO = "Q2-2026-INV-SETTLE"
EXPECTED_DATE = date(2026, 5, 8)


def check(env):
    failures = []

    partner = env["res.partner"].search([("name", "=", PARTNER_NAME)], limit=1)
    if not partner:
        return [f"Partner '{PARTNER_NAME}' not found"]

    # Target invoice checks
    invoice = env["account.move"].search([
        ("partner_id", "=", partner.id),
        ("ref", "=", TARGET_REF),
        ("move_type", "=", "out_invoice"),
    ], limit=1)
    if not invoice:
        return [f"Invoice '{TARGET_REF}' not found"]

    if invoice.payment_state not in ("in_payment", "paid"):
        failures.append(
            f"Invoice payment_state is '{invoice.payment_state}', expected 'in_payment' or 'paid'"
        )

    # Check the linked payment
    payments = invoice._get_reconciled_payments()
    if not payments:
        failures.append("No payment found linked to the target invoice")
    else:
        if len(payments) > 1:
            failures.append(f"Expected 1 payment, found {len(payments)}")
        payment = payments[0]
        if payment.memo != EXPECTED_MEMO:
            failures.append(
                f"Payment memo is '{payment.memo}', expected '{EXPECTED_MEMO}'"
            )
        if payment.date != EXPECTED_DATE:
            failures.append(
                f"Payment date is {payment.date}, expected {EXPECTED_DATE}"
            )

    # Distractor invoice must remain unpaid
    distractor = env["account.move"].search([
        ("partner_id", "=", partner.id),
        ("ref", "=", DISTRACTOR_REF),
        ("move_type", "=", "out_invoice"),
    ], limit=1)
    if not distractor:
        failures.append(f"Distractor invoice '{DISTRACTOR_REF}' not found")
    elif distractor.payment_state not in ("not_paid", "nothing"):
        failures.append(
            f"Distractor invoice was paid (payment_state='{distractor.payment_state}')"
        )

    return failures
