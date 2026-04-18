"""Seed for website_hr_recruitment.publish_job_from_backoffice_then_apply_portal.

Category: closed-loop cross-module (back-office <-> public portal).

NO pre-existing job is seeded for this task — the agent must create the
"Senior Widget Engineer" job in the back-office, publish it, then apply
to it on the public website.

Cleanup of any prior runs is performed first so the task is idempotent.
"""

JOB_NAME = "Senior Widget Engineer"
APPLICANT_NAME = "Alex Portal"
APPLICANT_EMAIL = "alex.portal@example.com"


def setup(env):
    # ----- Cleanup prior runs -----
    # Delete any applicants from previous runs (matches by name OR email).
    old_apps = env["hr.applicant"].search([
        "|",
        ("partner_name", "=", APPLICANT_NAME),
        ("email_from", "=", APPLICANT_EMAIL),
    ])
    if old_apps:
        old_apps.unlink()

    # Delete any leftover job named "Senior Widget Engineer" (and its
    # applicants, which we just unlinked above by email/name).
    old_jobs = env["hr.job"].with_context(active_test=False).search([
        ("name", "=", JOB_NAME),
    ])
    if old_jobs:
        # Unlink applicants attached to these jobs first.
        env["hr.applicant"].with_context(active_test=False).search([
            ("job_id", "in", old_jobs.ids),
        ]).unlink()
        old_jobs.unlink()

    # Verify the "Administration" department exists (it is part of base
    # hr_data demo data). If somehow missing, create it so the agent has
    # the right option.
    admin_dept = env["hr.department"].search([("name", "=", "Administration")], limit=1)
    if not admin_dept:
        env["hr.department"].create({"name": "Administration"})
