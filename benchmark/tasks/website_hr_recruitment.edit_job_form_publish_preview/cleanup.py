"""Cleanup for website_hr_recruitment.edit_job_form_publish_preview."""

JOB_NAME = "Bench QA Engineer"


def cleanup(env):
    jobs = env["hr.job"].with_context(active_test=False).search([
        ("name", "=", JOB_NAME),
    ])
    if jobs:
        env["hr.applicant"].with_context(active_test=False).search([
            ("job_id", "in", jobs.ids),
        ]).unlink()
        jobs.unlink()
