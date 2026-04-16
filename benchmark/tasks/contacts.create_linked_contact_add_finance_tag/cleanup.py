"""Clean up artifacts from previous runs."""


def cleanup(env):
    env["res.partner"].search([("name", "=", "Dana Patel")]).unlink()
