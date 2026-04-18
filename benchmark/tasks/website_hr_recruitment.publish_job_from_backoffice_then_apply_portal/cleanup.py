"""Cleanup for website_hr_recruitment.publish_job_from_backoffice_then_apply_portal."""


JOB_NAME = "Senior Widget Engineer"
APPLICANT_NAME = "Alex Portal"
APPLICANT_EMAIL = "alex.portal@example.com"


def cleanup(env):
    # Remove applicants
    env["hr.applicant"].with_context(active_test=False).search([
        "|",
        ("partner_name", "=", APPLICANT_NAME),
        ("email_from", "=", APPLICANT_EMAIL),
    ]).unlink()
    # Remove jobs
    jobs = env["hr.job"].with_context(active_test=False).search([
        ("name", "=", JOB_NAME),
    ])
    if jobs:
        env["hr.applicant"].with_context(active_test=False).search([
            ("job_id", "in", jobs.ids),
        ]).unlink()
        jobs.unlink()
