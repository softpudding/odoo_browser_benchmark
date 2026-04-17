"""Clean up artifacts from previous runs."""


def cleanup(env):
    env["crm.lead"].search([("name", "=", "Summit Energy Expansion")]).unlink()
