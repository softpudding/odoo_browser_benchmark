"""Clean up artifacts from previous runs."""


def cleanup(env):
    env["crm.lead"].search([("name", "=", "Vertex Renewal Expansion")]).unlink()
