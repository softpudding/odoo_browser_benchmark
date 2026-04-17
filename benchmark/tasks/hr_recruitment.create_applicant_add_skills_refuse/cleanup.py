"""Clean up artifacts from previous runs."""


def cleanup(env):
    applicants = env["hr.applicant"].with_context(active_test=False).search([
        ("partner_name", "in", ["Cameron Blake", "Cameron Brooks"]),
    ])
    for app in applicants:
        app.applicant_skill_ids.unlink()
        env["mail.message"].search([
            ("model", "=", "hr.applicant"),
            ("res_id", "=", app.id),
        ]).unlink()
    applicants.unlink()
