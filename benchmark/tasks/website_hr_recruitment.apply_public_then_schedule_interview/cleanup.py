"""Cleanup for website_hr_recruitment.apply_public_then_schedule_interview."""


APPLICANT_NAME = "Casey Portal"
APPLICANT_EMAIL = "casey.portal@example.com"


def cleanup(env):
    applicants = env["hr.applicant"].with_context(active_test=False).search([
        "|",
        ("partner_name", "=", APPLICANT_NAME),
        ("email_from", "=", APPLICANT_EMAIL),
    ])
    if applicants:
        env["mail.activity"].search([
            ("res_model", "=", "hr.applicant"),
            ("res_id", "in", applicants.ids),
        ]).unlink()
        applicants.unlink()
