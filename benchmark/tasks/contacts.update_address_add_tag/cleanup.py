"""Clean up artifacts from previous runs."""

COMPANY_NAME = "Brookfield Dynamics"


def cleanup(env):
    partners = env["res.partner"].search([("name", "=", COMPANY_NAME)])
    partners.unlink()
