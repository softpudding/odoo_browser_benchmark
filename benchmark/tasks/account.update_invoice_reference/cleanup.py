"""Clean up artifacts from previous runs."""

PARTNER_NAME = "Asterline Consulting"
INVOICE_REFS = ("BENCH-INV-REF-01", "BENCH-INV-REF-01-UPDATED")


def cleanup(env):
    # Remove test invoice records and reset environment to a clean baseline.
    partner = env["res.partner"].search([("name", "=", PARTNER_NAME)], limit=1)
    if not partner:
        return

    invs = env["account.move"].search([
        ("partner_id", "=", partner.id),
        "|",
        ("ref", "=", INVOICE_REFS[0]),
        ("ref", "=", INVOICE_REFS[1]),
    ])
    invs.unlink()
