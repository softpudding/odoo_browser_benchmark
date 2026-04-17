"""Cleanup for contacts.add_bank_account_to_partner."""

PARTNER_NAME = "Benchmark IBAN Supplier Ltd"


def cleanup(env):
    partner = env["res.partner"].search([("name", "=", PARTNER_NAME)], limit=1)
    if partner:
        env["res.partner.bank"].search([("partner_id", "=", partner.id)]).unlink()
