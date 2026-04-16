"""Clean up artifacts from previous runs."""

CONTACT_NAME = "Nora Patel"


def cleanup(env):
    env["res.partner"].search([("name", "=", CONTACT_NAME)]).unlink()
