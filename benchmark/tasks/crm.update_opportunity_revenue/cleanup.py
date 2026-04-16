"""Clean up artifacts from previous runs."""

OPP_NAME = "BENCH-OPP-REV-01"


def cleanup(env):
    env["crm.lead"].search([("name", "=", OPP_NAME)]).unlink()
