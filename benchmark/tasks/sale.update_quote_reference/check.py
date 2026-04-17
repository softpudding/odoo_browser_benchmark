"""Postcondition checks for sale.update_quote_reference."""

PARTNER_NAME = "Summitline Software"
NEW_REF = "BENCH-QREF-01-UPDATED"


def check(env):
    failures = []

    partner = env["res.partner"].search([("name", "=", PARTNER_NAME)], limit=1)
    if not partner:
        return [f"Customer '{PARTNER_NAME}' not found"]

    quotation = env["sale.order"].search([
        ("partner_id", "=", partner.id),
        ("client_order_ref", "=", NEW_REF),
        ("state", "=", "draft"),
    ], limit=1)
    if not quotation:
        return [f"Draft quotation with reference '{NEW_REF}' for '{PARTNER_NAME}' not found"]

    if len(quotation.order_line) != 1:
        failures.append(f"Expected 1 order line, found {len(quotation.order_line)}")

    return failures
