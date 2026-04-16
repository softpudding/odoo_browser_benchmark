"""Postcondition checks for contacts.update_contact_email."""

CONTACT_NAME = "Avery Dalton"
TARGET_EMAIL = "avery.dalton+ops@example.com"
TARGET_PHONE = "+1 555 0199"


def check(env):
    failures = []

    contact = env["res.partner"].search([("name", "=", CONTACT_NAME)], limit=1)
    if not contact:
        return [f"Contact '{CONTACT_NAME}' not found"]

    if (contact.email or "") != TARGET_EMAIL:
        failures.append(
            f"Email is {contact.email!r}, expected {TARGET_EMAIL!r}"
        )

    if (contact.phone or "") != TARGET_PHONE:
        failures.append(
            f"Phone is {contact.phone!r}, expected {TARGET_PHONE!r}"
        )

    return failures
