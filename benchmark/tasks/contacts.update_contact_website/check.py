"""Postcondition checks for contacts.update_contact_website."""

CONTACT_NAME = "Lena Porter"
TARGET_WEBSITE = "https://www.lena-porter.example.com"
EXPECTED_EMAIL = "lena.porter@example.com"


def check(env):
    failures = []

    contact = env["res.partner"].search([("name", "=", CONTACT_NAME)], limit=1)
    if not contact:
        return [f"Contact '{CONTACT_NAME}' not found"]

    if (contact.website or "").strip() != TARGET_WEBSITE:
        failures.append(
            f"Website is '{contact.website}', expected '{TARGET_WEBSITE}'"
        )

    if (contact.email or "").strip() != EXPECTED_EMAIL:
        failures.append(
            f"Email is '{contact.email}', expected '{EXPECTED_EMAIL}'"
        )

    return failures
