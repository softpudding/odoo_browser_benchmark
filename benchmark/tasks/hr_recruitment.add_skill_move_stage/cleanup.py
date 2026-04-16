"""Clean up artifacts from previous runs."""


def cleanup(env):
    applicants = env["hr.applicant"].search([
        ("partner_name", "=", "Jordan Park"),
    ])
    applicants.applicant_skill_ids.unlink()
    applicants.unlink()
