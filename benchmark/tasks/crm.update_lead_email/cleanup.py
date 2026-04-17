"""Clean up artifacts from previous runs."""

LEAD_NAME = "Cobalt Cloud Expansion"


def cleanup(env):
    env["crm.lead"].search([("name", "=", LEAD_NAME)]).unlink()
