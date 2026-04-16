"""Postcondition checks for account.update_invoice_reference."""

PARTNER_NAME = "Asterline Consulting"
NEW_REF = "BENCH-INV-REF-01-UPDATED"
OLD_REF = "BENCH-INV-REF-01"


def check(env):
    failures = []

    partner = env["res.partner"].search([("name", "=", PARTNER_NAME)], limit=1)
    if not partner:
        return [f"Partner '{PARTNER_NAME}' not found"]

    old_invoice = env["account.move"].search([
        ("partner_id", "=", partner.id),
        ("ref", "=", OLD_REF),
        ("state", "=", "draft"),
    ], limit=1)
    if old_invoice:
        failures.append(
            f"Invoice was not updated: reference is still '{OLD_REF}'"
        )

    invoice = env["account.move"].search([
        ("partner_id", "=", partner.id),
        ("ref", "=", NEW_REF),
    ], limit=1)
    if not invoice:
        return [f"Invoice with reference '{NEW_REF}' not found for '{PARTNER_NAME}'"]

    if invoice.state != "draft":
        failures.append(f"Invoice state is '{invoice.state}', expected 'draft'")

    if float(invoice.amount_total) != 600.0:
        failures.append(
            f"Invoice total is '{invoice.amount_total}', expected 600.0"
        )

    return failures
