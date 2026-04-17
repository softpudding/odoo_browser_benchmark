"""Seed a contact for the update-contact-mobile task."""

CONTACT_NAME = "Milo Reyes"
ORIGINAL_WEBSITE = "https://www.milo.example.com"
ORIGINAL_PHONE = "+1 555 0141"
ORIGINAL_EMAIL = "milo.reyes@example.com"


def setup(env):
    env["res.partner"].search([("name", "=", CONTACT_NAME)]).unlink()

    env["res.partner"].create({
        "name": CONTACT_NAME,
        "company_type": "person",
        "email": ORIGINAL_EMAIL,
        "phone": ORIGINAL_PHONE,
        "website": ORIGINAL_WEBSITE,
    })
