"""Postcondition checks for crm.lead_set_contact_name_email_phone_save.

Validates:
1. Lead 'Bench Lead Basic' still exists and is type='lead'.
2. contact_name == 'Alice Example'.
3. email_from == 'alice@example.com'.
4. phone contains '555-0200' (tolerates formatting variations).
"""

LEAD_NAME = "Bench Lead Basic"
EXPECTED_CONTACT_NAME = "Alice Example"
EXPECTED_EMAIL = "alice@example.com"
EXPECTED_PHONE_SUBSTR = "555-0200"


def check(env):
    failures = []

    leads = env["crm.lead"].with_context(active_test=False).search([
        ("name", "=", LEAD_NAME),
    ])
    if not leads:
        return [f"Lead '{LEAD_NAME}' not found"]
    if len(leads) > 1:
        failures.append(
            f"Expected exactly one '{LEAD_NAME}' lead, found {len(leads)}"
        )
    lead = leads[0]

    if not lead.active:
        failures.append("Lead is archived (active=False); expected active=True")

    if lead.type != "lead":
        failures.append(
            f"Record type is '{lead.type}', expected 'lead' "
            f"(agent may have converted to opportunity)"
        )

    actual_contact = (lead.contact_name or "").strip()
    if actual_contact != EXPECTED_CONTACT_NAME:
        failures.append(
            f"contact_name is '{actual_contact}', expected '{EXPECTED_CONTACT_NAME}'"
        )

    actual_email = (lead.email_from or "").strip().lower()
    if actual_email != EXPECTED_EMAIL:
        failures.append(
            f"email_from is '{lead.email_from}', expected '{EXPECTED_EMAIL}'"
        )

    actual_phone = (lead.phone or "").strip()
    if EXPECTED_PHONE_SUBSTR not in actual_phone:
        failures.append(
            f"phone is '{actual_phone}', expected to contain '{EXPECTED_PHONE_SUBSTR}'"
        )

    # Guardrail — do not silently change the lead's name
    if lead.name != LEAD_NAME:
        failures.append(
            f"Lead name is '{lead.name}', expected '{LEAD_NAME}'"
        )

    return failures
