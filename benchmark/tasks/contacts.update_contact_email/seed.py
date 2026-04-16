"""Seed a contact for the contact-email update task."""

CONTACT_NAME = "Avery Dalton"
ORIGINAL_EMAIL = "avery.dalton@example.com"
TARGET_PHONE = "+1 555 0199"


def setup(env):
    env["res.partner"].search([("name", "=", CONTACT_NAME)]).unlink()

    env["res.partner"].create({
        "name": CONTACT_NAME,
        "company_type": "person",
        "email": ORIGINAL_EMAIL,
        "phone": TARGET_PHONE,
    })
