"""Postconditions for contacts.add_bank_account_iban."""

PARTNER_NAME = "Ridgeway Commercial Services"
IBAN = "DE89370400440532013000"


def check(env):
    failures = []

    partner = env["res.partner"].search([("name", "=", PARTNER_NAME)], limit=1)
    if not partner:
        return [f"Partner '{PARTNER_NAME}' not found"]

    banks = env["res.partner.bank"].search([("partner_id", "=", partner.id)])
    if not banks:
        return [
            f"Partner '{PARTNER_NAME}' has no bank accounts — agent likely "
            f"did not submit the create dialog"
        ]

    if len(banks) > 1:
        failures.append(
            f"Partner has {len(banks)} bank accounts, expected exactly 1"
        )

    target = banks.filtered(lambda b: b.acc_number == IBAN)
    if not target:
        failures.append(
            f"No bank account with acc_number '{IBAN}' on this partner; "
            f"found {banks.mapped('acc_number')}"
        )

    return failures
