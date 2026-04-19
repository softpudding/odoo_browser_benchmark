"""Seed for website_hr_recruitment.apply_public_then_schedule_interview.

Category: closed-loop cross-module (public website -> back-office).

Seeds a *published* job position so the public /jobs page shows it. The agent
must then:
  1. Submit an application on the public website (no login), and
  2. Log in as admin and schedule a Meeting activity via the chatter on the
     newly-created applicant.

Browser-use typically fails at one of:
  * Navigating between the public portal and the back-office in one run.
  * Opening the chatter "Activity" popover and setting Activity Type = Meeting
    (the default is "To-Do") + a specific date_deadline via Odoo's date picker.
"""

JOB_NAME = "Senior Backend Engineer"
APPLICANT_NAME = "Bench Candidate"
APPLICANT_EMAIL = "bench.candidate@example.com"
STAGE_NAME = "Initial Qualification"


def setup(env):
    # ------------------------------------------------------------------
    # 1. Cleanup prior runs (by email or name, handles partial prior runs)
    # ------------------------------------------------------------------
    old_apps = env["hr.applicant"].with_context(active_test=False).search([
        "|",
        ("partner_name", "=", APPLICANT_NAME),
        ("email_from", "=", APPLICANT_EMAIL),
    ])
    if old_apps:
        env["mail.activity"].search([
            ("res_model", "=", "hr.applicant"),
            ("res_id", "in", old_apps.ids),
        ]).unlink()
        old_apps.unlink()

    # Stray Interview activities that may have been left behind
    env["mail.activity"].search([
        ("res_model", "=", "hr.applicant"),
        ("summary", "=", "Interview"),
    ]).unlink()

    # ------------------------------------------------------------------
    # 2. Ensure Administration department exists (common base data).
    # ------------------------------------------------------------------
    dept = env["hr.department"].search(
        [("name", "=", "Administration")], limit=1
    )
    if not dept:
        dept = env["hr.department"].create({"name": "Administration"})

    # ------------------------------------------------------------------
    # 3. Ensure hr.job "Senior Backend Engineer" exists and is published.
    # ------------------------------------------------------------------
    job = env["hr.job"].with_context(active_test=False).search(
        [("name", "=", JOB_NAME)], limit=1
    )
    if not job:
        job = env["hr.job"].create({
            "name": JOB_NAME,
            "department_id": dept.id,
            "no_of_recruitment": 1,
            "is_published": True,
            "website_published": True,
            "description": (
                "<p>Build and maintain server-side services. "
                "Strong Python + PostgreSQL experience required.</p>"
            ),
        })
    else:
        job.write({
            "active": True,
            "department_id": dept.id,
            "no_of_recruitment": 1,
            "is_published": True,
            "website_published": True,
        })

    # ------------------------------------------------------------------
    # 4. Ensure the Initial Qualification stage exists for this job.
    # ------------------------------------------------------------------
    stage = env["hr.recruitment.stage"].search(
        [("name", "=", STAGE_NAME)], limit=1
    )
    if not stage:
        stage = env["hr.recruitment.stage"].create({
            "name": STAGE_NAME,
            "sequence": 10,
            "job_ids": [(4, job.id)],
        })
    elif job not in stage.job_ids:
        stage.write({"job_ids": [(4, job.id)]})
