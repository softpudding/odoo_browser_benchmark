"""Seed for contacts.add_bank_account_to_partner."""

PARTNER_NAME = "Benchmark IBAN Supplier Ltd"


def setup(env):
    # Clean prior bank accounts under the partner.
    partner = env["res.partner"].search([("name", "=", PARTNER_NAME)], limit=1)
    if partner:
        env["res.partner.bank"].search([("partner_id", "=", partner.id)]).unlink()
    else:
        partner = env["res.partner"].create({
            "name": PARTNER_NAME,
            "is_company": True,
            "supplier_rank": 1,
            "email": "accounts@benchmark-iban.example",
        })
