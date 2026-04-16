"""Postcondition checks for account.partial_pay_vendor_bill_with_memo."""

from math import isclose


VENDOR_NAME = "Summit Office Supply"
TARGET_REF = "VB-PARTIAL-01"
DISTRACTOR_REF = "VB-PARTIAL-02"
EXPECTED_MEMO = "PARTIAL-JUN-600"


def check(env):
    failures = []

    vendor = env["res.partner"].search([("name", "=", VENDOR_NAME)], limit=1)
    if not vendor:
        return [f"Vendor '{VENDOR_NAME}' not found"]

    bill = env["account.move"].search([
        ("move_type", "=", "in_invoice"),
        ("partner_id", "=", vendor.id),
        ("ref", "=", TARGET_REF),
    ], limit=1)
    if not bill:
        return [f"Target bill '{TARGET_REF}' not found"]

    payments = bill._get_reconciled_payments()
    if len(payments) != 1:
        failures.append(f"Expected 1 linked payment on target bill, found {len(payments)}")
    else:
        payment = payments[0]
        if payment.memo != EXPECTED_MEMO:
            failures.append(f"Payment memo is '{payment.memo}', expected '{EXPECTED_MEMO}'")
        if str(payment.date) != "2026-06-12":
            failures.append(f"Payment date is {payment.date}, expected 2026-06-12")
        if not isclose(float(payment.amount), 600.0, rel_tol=0.0, abs_tol=0.01):
            failures.append(f"Payment amount is {payment.amount}, expected 600.00")

    if not isclose(float(bill.amount_residual), 300.0, rel_tol=0.0, abs_tol=0.01):
        failures.append(f"Target bill residual is {bill.amount_residual}, expected 300.00")

    distractor = env["account.move"].search([
        ("move_type", "=", "in_invoice"),
        ("partner_id", "=", vendor.id),
        ("ref", "=", DISTRACTOR_REF),
    ], limit=1)
    if not distractor:
        failures.append(f"Distractor bill '{DISTRACTOR_REF}' not found")
    elif distractor._get_reconciled_payments():
        failures.append("Distractor bill should not have any linked payments")

    return failures
