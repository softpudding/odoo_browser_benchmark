"""Seed a contact for the website-update task."""

CONTACT_NAME = "Lena Porter"
ORIGINAL_WEBSITE = "http://www.lena.example.com"


def setup(env):
    env["res.partner"].search([("name", "=", CONTACT_NAME)]).unlink()

    env["res.partner"].create({
        "name": CONTACT_NAME,
        "company_type": "person",
        "email": "lena.porter@example.com",
        "phone": "+1 555 0148",
        "website": ORIGINAL_WEBSITE,
    })
