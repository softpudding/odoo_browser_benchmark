"""Clean up artifacts from previous runs."""

TARGET_PARTNER = "Acme Corporation"


def cleanup(env):
    opps = env["crm.lead"].search([("partner_name", "=", TARGET_PARTNER)])
    opps.unlink()
