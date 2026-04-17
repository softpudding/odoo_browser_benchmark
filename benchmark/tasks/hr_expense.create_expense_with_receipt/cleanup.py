"""Clean up artifacts from previous runs."""


def cleanup(env):
    env["hr.expense"].search([
        ("name", "=", "Client dinner at Harborview"),
    ]).unlink()
