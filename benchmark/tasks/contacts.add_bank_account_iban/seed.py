"""Seed for contacts.add_bank_account_iban.

Category: deep_ui_interaction (MEDIUM).
Seeds a company partner without any bank account. The agent must open
the partner, switch to the Invoicing tab, and add a bank account with
the exact IBAN through the many2many_tags_banks create dialog.
"""

PARTNER_NAME = "Ridgeway Commercial Services"
IBAN = "DE89370400440532013000"


def setup(env):
    Partner = env["res.partner"]
    Bank = env["res.partner.bank"]

    # Cleanup prior runs — remove any bank accounts with our IBAN first, then
    # the partner (partner removal won't cascade to banks belonging to others).
    stale_banks = Bank.search([("acc_number", "=", IBAN)])
    stale_banks.unlink()

    stale_partners = Partner.search([("name", "=", PARTNER_NAME)])
    stale_partners.unlink()

    # Create the partner.
    Partner.create({
        "name": PARTNER_NAME,
        "is_company": True,
        "street": "88 Ridgeway Road",
        "city": "Bremen",
        "zip": "28195",
        "country_id": env.ref("base.de").id,
        "email": "accounts@ridgeway-commercial.example",
        "phone": "+49 421 5550198",
    })
