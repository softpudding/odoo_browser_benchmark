"""Postcondition checks for contacts.update_contact_mobile."""

CONTACT_NAME = "Milo Reyes"
TARGET_WEBSITE = "https://www.miloreyes.example.com"
ORIGINAL_PHONE = "+1 555 0141"
ORIGINAL_EMAIL = "milo.reyes@example.com"


def check(env):
    failures = []

    contact = env["res.partner"].search([("name", "=", CONTACT_NAME)], limit=1)
    if not contact:
        return [f"Contact '{CONTACT_NAME}' not found"]

    if (contact.website or "") != TARGET_WEBSITE:
        failures.append(
            f"Website is '{contact.website}', expected '{TARGET_WEBSITE}'"
        )

    if (contact.phone or "") != ORIGINAL_PHONE:
        failures.append(
            f"Phone changed to '{contact.phone}', expected '{ORIGINAL_PHONE}'"
        )

    if (contact.email or "") != ORIGINAL_EMAIL:
        failures.append(
            f"Email changed to '{contact.email}', expected '{ORIGINAL_EMAIL}'"
        )

    return failures
