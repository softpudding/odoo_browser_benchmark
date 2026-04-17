"""Clean up artifacts from previous runs."""

CONTACT_NAME = "Lena Porter"


def cleanup(env):
    env["res.partner"].search([("name", "=", CONTACT_NAME)]).unlink()
