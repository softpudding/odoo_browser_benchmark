"""Postcondition checks for sale.create_invoice_register_payment_memo."""

from datetime import date


PARTNER_NAME = "Brightwave Labs"
TARGET_REF = "PAYFLOW-01"
DISTRACTOR_REF = "PAYFLOW-02"
EXPECTED_MEMO = "PAYFLOW-MAY-SETTLEMENT"
EXPECTED_DATE = date(2026, 5, 21)


def check(env):
    failures = []

    partner = env["res.partner"].search([("name", "=", PARTNER_NAME)], limit=1)
    if not partner:
        return [f"Partner '{PARTNER_NAME}' not found"]

    order = env["sale.order"].search([
        ("partner_id", "=", partner.id),
        ("client_order_ref", "=", TARGET_REF),
    ], limit=1)
    distractor = env["sale.order"].search([
        ("partner_id", "=", partner.id),
        ("client_order_ref", "=", DISTRACTOR_REF),
    ], limit=1)
    if not order or not distractor:
        return ["Missing seeded sales orders for payflow task"]

    if order.state != "sale":
        failures.append(f"Target order state is {order.state!r}, expected 'sale'")
    if order.invoice_status != "invoiced":
        failures.append(
            f"Target order invoice_status is {order.invoice_status!r}, expected 'invoiced'"
        )

    invoices = order.invoice_ids.filtered(lambda move: move.move_type == "out_invoice")
    if len(invoices) != 1:
        failures.append(f"Expected 1 invoice on target order, found {len(invoices)}")
        return failures

    invoice = invoices[0]
    if invoice.state != "posted":
        failures.append(f"Invoice state is {invoice.state!r}, expected 'posted'")
    if invoice.payment_state not in ("in_payment", "paid"):
        failures.append(
            f"Invoice payment_state is {invoice.payment_state!r}, expected 'in_payment' or 'paid'"
        )

    payments = invoice._get_reconciled_payments()
    if len(payments) != 1:
        failures.append(f"Expected 1 payment linked to the invoice, found {len(payments)}")
    else:
        payment = payments[0]
        if payment.memo != EXPECTED_MEMO:
            failures.append(
                f"Payment memo is {payment.memo!r}, expected {EXPECTED_MEMO!r}"
            )
        if payment.date != EXPECTED_DATE:
            failures.append(
                f"Payment date is {payment.date!r}, expected {EXPECTED_DATE!r}"
            )

    if distractor.invoice_ids.filtered(lambda move: move.move_type == "out_invoice"):
        failures.append("Distractor sales order was invoiced")

    return failures
