"""Postcondition checks for account.register_payment_defaults."""


def check(env):
    failures = []

    partner = env["res.partner"].search(
        [("name", "=", "Lakeview Partners")], limit=1
    )
    if not partner:
        return ["Partner 'Lakeview Partners' not found"]

    invoice = env["account.move"].search([
        ("ref", "=", "BENCH-PAY-01"),
        ("partner_id", "=", partner.id),
    ], limit=1)
    if not invoice:
        return ["Invoice with ref 'BENCH-PAY-01' not found for Lakeview Partners"]

    if invoice.state != "posted":
        failures.append(
            f"Invoice state is {invoice.state!r}, expected 'posted'"
        )

    if invoice.payment_state not in ("paid", "in_payment"):
        failures.append(
            f"Invoice payment_state is {invoice.payment_state!r}, "
            f"expected 'paid' or 'in_payment'"
        )

    if invoice.amount_total != 1000.0:
        failures.append(
            f"Invoice amount_total is {invoice.amount_total}, expected 1000.0"
        )

    return failures
