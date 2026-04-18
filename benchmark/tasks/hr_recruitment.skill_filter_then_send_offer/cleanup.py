"""Clean up artifacts from previous runs."""

NAMES = [
    "Alice Senior",
    "Bob Junior",
    "Dana Pirate",
    "Eve Contractor",
    "Charlie Jones",
]


def cleanup(env):
    Applicant = env["hr.applicant"].with_context(active_test=False)
    apps = Applicant.search([("partner_name", "in", NAMES)])
    for app in apps:
        app.applicant_skill_ids.unlink()
        env["mail.message"].sudo().search([
            ("model", "=", "hr.applicant"),
            ("res_id", "=", app.id),
        ]).unlink()
    apps.unlink()
