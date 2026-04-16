"""Postcondition checks for account.register_payment_defaults.

Validates that:
1. The invoice payment_state changed to 'paid' or 'in_payment'
2. A payment of $1,000.00 was created
3. The payment is linked to the correct invoice
"""


def check(env):
    failures = []

    # Find the partner
    partner = env["res.partner"].search(
        [("name", "=", "Lakeview Partners")], limit=1
    )
    if not partner:
        return ["Partner 'Lakeview Partners' not found"]

    # Find the target invoice
    invoice = env["account.move"].search([
        ("ref", "=", "BENCH-PAY-01"),
        ("partner_id", "=", partner.id),
    ], limit=1)
    if not invoice:
        return ["Invoice with ref 'BENCH-PAY-01' not found for Lakeview Partners"]

    # Check invoice is posted
    if invoice.state != "posted":
        failures.append(
            f"Invoice state is {invoice.state!r}, expected 'posted'"
        )

    # Check payment_state changed to paid or in_payment
    if invoice.payment_state not in ("paid", "in_payment"):
        failures.append(
            f"Invoice payment_state is {invoice.payment_state!r}, "
            f"expected 'paid' or 'in_payment'"
        )

    # Check a payment of $1,000.00 was created
    payments = env["account.payment"].search([
        ("memo", "=", "BENCH-PAY-01"),
    ])
    if not payments:
        failures.append("No payment found with memo 'BENCH-PAY-01'")
    else:
        for pmt in payments:
            if pmt.amount != 1000.0:
                failures.append(
                    f"Payment amount is {pmt.amount}, expected 1000.0"
                )
            if pmt.state != "posted":
                failures.append(
                    f"Payment state is {pmt.state!r}, expected 'posted'"
                )

    # Verify the invoice total is $1,000.00
    if invoice.amount_total != 1000.0:
        failures.append(
            f"Invoice amount_total is {invoice.amount_total}, expected 1000.0"
        )

    return failures
