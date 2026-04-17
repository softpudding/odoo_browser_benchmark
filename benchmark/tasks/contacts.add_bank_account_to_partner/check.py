"""Postcondition checks for contacts.add_bank_account_to_partner."""

import re

PARTNER_NAME = "Benchmark IBAN Supplier Ltd"
EXPECTED_IBAN_NORMALIZED = "GB82WEST12345698765432"


def check(env):
    failures = []

    partner = env["res.partner"].search([("name", "=", PARTNER_NAME)], limit=1)
    if not partner:
        return [f"Partner '{PARTNER_NAME}' not found"]

    banks = env["res.partner.bank"].search([("partner_id", "=", partner.id)])
    if not banks:
        return [f"No bank account linked to '{PARTNER_NAME}'"]
    if len(banks) > 1:
        failures.append(f"Expected 1 bank account, found {len(banks)}")

    for b in banks:
        normalized = re.sub(r"\s+", "", (b.acc_number or "")).upper()
        if normalized != EXPECTED_IBAN_NORMALIZED:
            failures.append(
                f"Bank account '{b.acc_number}' does not match "
                f"expected IBAN '{EXPECTED_IBAN_NORMALIZED}'"
            )

    return failures
