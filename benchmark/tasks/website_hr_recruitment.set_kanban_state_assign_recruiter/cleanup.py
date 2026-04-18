"""Clean up artifacts from previous runs.

Removes Diana Recruit applicant and the chatter/activities attached to her.
Recruiter Bob and the job position are kept (they are part of the seeded
fixture and may be re-used by repeated runs).
"""

APPLICANT_NAME = "Diana Recruit"


def cleanup(env):
    apps = env["hr.applicant"].with_context(active_test=False).search([
        ("partner_name", "=", APPLICANT_NAME),
    ])
    if apps:
        env["mail.message"].search([
            ("model", "=", "hr.applicant"),
            ("res_id", "in", apps.ids),
        ]).sudo().unlink()
        env["mail.activity"].search([
            ("res_model", "=", "hr.applicant"),
            ("res_id", "in", apps.ids),
        ]).sudo().unlink()
        apps.sudo().unlink()
