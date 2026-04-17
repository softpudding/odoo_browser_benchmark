"""Clean up artifacts from previous runs."""

CUSTOMER_NAME = "Summitline Software"
NEW_REF = "BENCH-QREF-01-UPDATED"
OLD_REF = "BENCH-QREF-01"


def cleanup(env):
    partner = env["res.partner"].search([("name", "=", CUSTOMER_NAME)], limit=1)
    if not partner:
        return

    for ref in (OLD_REF, NEW_REF):
        env["sale.order"].search([
            ("partner_id", "=", partner.id),
            ("client_order_ref", "=", ref),
        ]).unlink()
