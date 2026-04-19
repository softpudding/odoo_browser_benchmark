"""Cleanup for website_hr_recruitment.apply_public_then_schedule_interview."""

JOB_NAME = "Senior Backend Engineer"
APPLICANT_NAME = "Bench Candidate"
APPLICANT_EMAIL = "bench.candidate@example.com"
ACTIVITY_SUMMARY = "Interview"


def cleanup(env):
    # Remove any 'Interview' activities on hr.applicant first.
    env["mail.activity"].search([
        ("res_model", "=", "hr.applicant"),
        ("summary", "=", ACTIVITY_SUMMARY),
    ]).unlink()

    # Remove applicants by name or email.
    apps = env["hr.applicant"].with_context(active_test=False).search([
        "|",
        ("partner_name", "=", APPLICANT_NAME),
        ("email_from", "=", APPLICANT_EMAIL),
    ])
    if apps:
        env["mail.activity"].search([
            ("res_model", "=", "hr.applicant"),
            ("res_id", "in", apps.ids),
        ]).unlink()
        apps.unlink()

    # Also clean activities on the job's remaining applicants in case prior
    # runs left stray data there.
    jobs = env["hr.job"].with_context(active_test=False).search(
        [("name", "=", JOB_NAME)]
    )
    if jobs:
        stray = env["hr.applicant"].with_context(active_test=False).search([
            ("job_id", "in", jobs.ids),
        ])
        if stray:
            env["mail.activity"].search([
                ("res_model", "=", "hr.applicant"),
                ("res_id", "in", stray.ids),
            ]).unlink()
            stray.unlink()
