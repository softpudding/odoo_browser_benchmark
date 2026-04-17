"""Clean up artifacts from previous runs of contacts.add_bank_account_iban."""

PARTNER_NAME = "Ridgeway Commercial Services"
IBAN = "DE89370400440532013000"


def cleanup(env):
    env["res.partner.bank"].search([("acc_number", "=", IBAN)]).unlink()
    env["res.partner"].search([("name", "=", PARTNER_NAME)]).unlink()
