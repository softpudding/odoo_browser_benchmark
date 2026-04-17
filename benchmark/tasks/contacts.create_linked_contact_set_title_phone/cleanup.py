"""Clean up artifacts from previous runs."""


def cleanup(env):
    env["res.partner"].search([("name", "=", "Leah Morgan")]).unlink()
