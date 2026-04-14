"""Clean up jobs and applicants from previous runs."""


def cleanup(env):
    env["hr.applicant"].search([("email_from", "=", "jack@doe.com")]).unlink()
    env["hr.job"].search([
        ("name", "in", [
            "Platform Support Specialist",
            "Platform Support Coordinator",
            "Customer Success Specialist",
        ]),
    ]).unlink()
    env["hr.department"].search([
        ("name", "in", ["Platform Ops", "Customer Success"]),
    ]).unlink()


