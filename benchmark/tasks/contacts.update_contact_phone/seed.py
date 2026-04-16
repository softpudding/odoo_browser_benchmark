"""Seed a contact for the update-contact-phone task."""

CONTACT_NAME = "Nora Patel"


def setup(env):
    env["res.partner"].search([("name", "=", CONTACT_NAME)]).unlink()

    env["res.partner"].create({
        "name": CONTACT_NAME,
        "email": "nora.patel@example.com",
        "phone": "+1 555 0102",
        "is_company": False,
    })
