"""Postcondition checks for account.create_customer_invoice_post."""

PARTNER_NAME = "Northwind Advisory"
INVOICE_REF = "NWA-AR-220"
EXPECTED_LINES = {
    "Strategic Workshop": (2.0, 1200.0),
    "Support Retainer": (1.0, 850.0),
}


def check(env):
    failures = []

    partner = env["res.partner"].search([("name", "=", PARTNER_NAME)], limit=1)
    if not partner:
        return [f"Partner '{PARTNER_NAME}' not found"]

    invoices = env["account.move"].search([
        ("move_type", "=", "out_invoice"),
        ("partner_id", "=", partner.id),
        ("ref", "=", INVOICE_REF),
    ])
    if len(invoices) != 1:
        return [f"Expected exactly 1 invoice with ref '{INVOICE_REF}', found {len(invoices)}"]

    invoice = invoices[0]
    if invoice.state != "posted":
        failures.append(f"Invoice state is '{invoice.state}', expected 'posted'")
    if str(invoice.invoice_date) != "2026-06-10":
        failures.append(
            f"Invoice date is {invoice.invoice_date}, expected 2026-06-10"
        )

    lines = invoice.invoice_line_ids.filtered(lambda line: not line.display_type)
    if len(lines) != 2:
        failures.append(f"Expected 2 invoice lines, found {len(lines)}")
    seen = {}
    for line in lines:
        seen[line.product_id.name] = (float(line.quantity), float(line.price_unit))
    for product_name, expected in EXPECTED_LINES.items():
        if product_name not in seen:
            failures.append(f"Missing invoice line for '{product_name}'")
            continue
        if seen[product_name] != expected:
            failures.append(
                f"Line '{product_name}' is {seen[product_name]}, expected {expected}"
            )

    return failures
