"""Clean up artifacts from previous runs."""


def cleanup(env):
    env["website.page"].search([("url", "=", "/about-us")]).unlink()