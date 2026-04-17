"""Clean up artifacts from previous runs."""


def cleanup(env):
    env["hr.employee"].search([("name", "=", "Lena Ortiz")]).unlink()
