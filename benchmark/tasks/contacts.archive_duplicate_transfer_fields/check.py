"""Postconditions for contacts.archive_duplicate_transfer_fields."""

PRIMARY_REF = "RGS-PRIMARY"
DUPLICATE_REF = "RGS-DUPLICATE"
PHONE = "+1 415 555 0188"
EMAIL = "contact@ridgeway-global.example"
STREET = "45 Market Street"
CITY = "San Francisco"


def check(env):
    failures = []

    Partner = env["res.partner"].with_context(active_test=False)

    primary = Partner.search([("ref", "=", PRIMARY_REF)], limit=1)
    duplicate = Partner.search([("ref", "=", DUPLICATE_REF)], limit=1)

    if not primary:
        return [f"Primary partner with ref '{PRIMARY_REF}' not found — "
                f"agent may have deleted it"]

    if not primary.active:
        failures.append("Primary partner is archived — should remain active")

    if primary.phone != PHONE:
        failures.append(
            f"Primary phone is '{primary.phone}', expected '{PHONE}'"
        )
    if primary.email != EMAIL:
        failures.append(
            f"Primary email is '{primary.email}', expected '{EMAIL}'"
        )
    if primary.street != STREET:
        failures.append(
            f"Primary street is '{primary.street}', expected '{STREET}'"
        )
    if primary.city != CITY:
        failures.append(
            f"Primary city is '{primary.city}', expected '{CITY}'"
        )

    if not duplicate:
        failures.append(
            f"Duplicate partner with ref '{DUPLICATE_REF}' no longer "
            f"exists — agent likely DELETED instead of archiving"
        )
    else:
        if duplicate.active:
            failures.append(
                f"Duplicate partner is still active — agent did not archive it"
            )

    return failures
