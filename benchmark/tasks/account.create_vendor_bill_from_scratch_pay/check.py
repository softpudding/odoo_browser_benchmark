"""Postcondition checks for account.create_vendor_bill_from_scratch_pay.

Validates the three sequential gates:
  1. Bill created: account.move with move_type='in_invoice',
     ref='BENCH-VBILL-001', vendor='Bench Bill Vendor', exactly one
     product line (Bench Bill Item qty=2 price=75 total=150.00),
     invoice_date=2026-05-10.
  2. Bill posted: state='posted'.
  3. Bill fully paid: payment_state='paid' (or 'in_payment' if the
     journal uses an outstanding account), with exactly one linked
     account.payment for amount=150.00, payment_type='outbound',
     payment state in ('posted', 'paid', 'in_process').
"""

from datetime import date


VENDOR_NAME = "Bench Bill Vendor"
PRODUCT_NAME = "Bench Bill Item"
TARGET_REF = "BENCH-VBILL-001"
EXPECTED_DATE = date(2026, 5, 10)
EXPECTED_TOTAL = 150.0
EXPECTED_QTY = 2
EXPECTED_PRICE = 75.0


def check(env):
    failures = []

    vendor = env["res.partner"].search(
        [("name", "=", VENDOR_NAME)], limit=1
    )
    if not vendor:
        return [f"Vendor '{VENDOR_NAME}' not found"]

    bill = env["account.move"].search([
        ("ref", "=", TARGET_REF),
        ("move_type", "=", "in_invoice"),
    ], limit=1)
    if not bill:
        return [
            f"Vendor bill with ref={TARGET_REF!r} and move_type='in_invoice' "
            f"not found — did the agent click New and fill the reference?"
        ]

    # --- Gate 1: bill header is correct ---
    if bill.partner_id.id != vendor.id:
        failures.append(
            f"Bill vendor is {bill.partner_id.name!r}, expected {VENDOR_NAME!r}"
        )
    if bill.invoice_date != EXPECTED_DATE:
        failures.append(
            f"Bill invoice_date is {bill.invoice_date!r}, "
            f"expected {EXPECTED_DATE!s} (05/10/2026)"
        )

    # --- Gate 1: exactly one product line, correct values ---
    product_lines = bill.invoice_line_ids.filtered(
        lambda l: (l.display_type in (False, "product"))
        and (l.product_id or l.name)
    )
    # Exclude fully-empty rows (phantom lines) defensively.
    product_lines = product_lines.filtered(lambda l: l.product_id)

    if len(product_lines) != 1:
        failures.append(
            f"Expected exactly 1 product line on the bill, found "
            f"{len(product_lines)}. Agent may have left a phantom empty "
            f"line or added an extra line."
        )
    else:
        line = product_lines[0]
        if line.product_id.name != PRODUCT_NAME:
            failures.append(
                f"Bill line product is {line.product_id.name!r}, "
                f"expected {PRODUCT_NAME!r}"
            )
        if abs(line.quantity - EXPECTED_QTY) > 0.001:
            failures.append(
                f"Bill line quantity is {line.quantity}, "
                f"expected {EXPECTED_QTY}"
            )
        if abs(line.price_unit - EXPECTED_PRICE) > 0.01:
            failures.append(
                f"Bill line price_unit is {line.price_unit}, "
                f"expected {EXPECTED_PRICE}"
            )

    if abs(bill.amount_total - EXPECTED_TOTAL) > 0.01:
        failures.append(
            f"Bill amount_total is {bill.amount_total}, "
            f"expected {EXPECTED_TOTAL} (qty 2 * price 75, taxes cleared)"
        )

    # --- Gate 2: bill posted ---
    if bill.state != "posted":
        failures.append(
            f"Bill state is {bill.state!r}, expected 'posted' "
            f"(did the agent click Confirm?)"
        )
        # Return early — downstream gates depend on a posted bill.
        return failures

    # --- Gate 3: bill paid, exactly one outbound payment linked ---
    # On the base snapshot's Bank journal the payment reconciles directly
    # against the payable, flipping the bill to 'paid'. Accept 'paid' or
    # 'in_payment' defensively.
    if bill.payment_state not in ("paid", "in_payment"):
        failures.append(
            f"Bill payment_state is {bill.payment_state!r}, "
            f"expected 'paid' (did the agent click Pay and then "
            f"Create Payment in the wizard?)"
        )

    payments = bill._get_reconciled_payments()
    if not payments:
        failures.append(
            "No payments linked to the bill — agent opened the wizard but "
            "did not create the payment, or clicked Discard."
        )
        return failures
    if len(payments) != 1:
        failures.append(
            f"Expected exactly 1 linked payment, found {len(payments)}"
        )

    pay = payments[0]
    if abs(pay.amount - EXPECTED_TOTAL) > 0.01:
        failures.append(
            f"Payment amount is {pay.amount}, expected {EXPECTED_TOTAL} "
            f"(agent should accept the wizard default full amount)"
        )
    if pay.payment_type != "outbound":
        failures.append(
            f"Payment payment_type is {pay.payment_type!r}, "
            f"expected 'outbound' (vendor bill payment)"
        )
    if pay.partner_id.id != vendor.id:
        failures.append(
            f"Payment partner is {pay.partner_id.name!r}, "
            f"expected {VENDOR_NAME!r}"
        )
    if pay.state not in ("posted", "paid", "in_process"):
        failures.append(
            f"Payment state is {pay.state!r}, expected one of "
            f"'posted', 'paid', 'in_process'"
        )

    return failures
