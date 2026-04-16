"""Clean up artifacts from previous runs."""


def cleanup(env):
    for name in ["Patricia Drum", "Steven Okafor", "Vantage Industrial Group"]:
        partners = env["res.partner"].search([("name", "=", name)])
        partners.unlink()
