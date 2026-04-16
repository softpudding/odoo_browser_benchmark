"""Clean up artifacts from previous runs."""

APPLICANT_NAME = "Taylor Kim"


def cleanup(env):
    apps = env["hr.applicant"].search([
        ("partner_name", "=", APPLICANT_NAME),
    ])
    apps.unlink()
