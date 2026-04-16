"""Postcondition checks for contacts.update_contact_phone."""

CONTACT_NAME = "Nora Patel"
TARGET_PHONE = "+1 555 0312"
EXPECTED_EMAIL = "nora.patel@example.com"


def check(env):
    failures = []

    contact = env["res.partner"].search([("name", "=", CONTACT_NAME)], limit=1)
    if not contact:
        return [f"Contact '{CONTACT_NAME}' not found"]

    if (contact.phone or "") != TARGET_PHONE:
        failures.append(
            f"Phone is '{contact.phone}', expected '{TARGET_PHONE}'"
        )

    if (contact.email or "") != EXPECTED_EMAIL:
        failures.append(
            f"Email changed to '{contact.email}', expected '{EXPECTED_EMAIL}'"
        )

    return failures
