"""Seed one job position with three active applicants.

Category 2 (MEDIUM): The agent must open the correct applicant among two
distractors, click Refuse, pick a specific refuse reason in the wizard,
uncheck Send Email, and submit the wizard.
"""


JOB_NAME = "Senior Platform Engineer"
APPLICANTS = [
    {"partner_name": "Marcus Whitfield", "email_from": "marcus.whitfield@example.com"},
    {"partner_name": "Ella Navarro", "email_from": "ella.navarro@example.com"},
    {"partner_name": "Devon Burke", "email_from": "devon.burke@example.com"},
]


def setup(env):
    # Cleanup prior runs — applicants on this job
    existing = env["hr.applicant"].with_context(active_test=False).search(
        [("job_id.name", "=", JOB_NAME)]
    )
    for app in existing:
        env["mail.message"].search([
            ("model", "=", "hr.applicant"),
            ("res_id", "=", app.id),
        ]).unlink()
        app.unlink()

    job = env["hr.job"].search([("name", "=", JOB_NAME)], limit=1)
    if not job:
        dept = env["hr.department"].search([("name", "=", "Engineering")], limit=1)
        if not dept:
            dept = env["hr.department"].create({"name": "Engineering"})
        job = env["hr.job"].create({
            "name": JOB_NAME,
            "department_id": dept.id,
        })

    # Make sure job is open / published so it shows in recruitment kanban
    if hasattr(job, "state") and job.state != "recruit":
        try:
            job.set_recruit()
        except Exception:
            pass

    # Pick the first refuse reason to ensure default exists; the oracle
    # will pick a specific one by name in the wizard.
    env["hr.applicant.refuse.reason"].search([("name", "=", "Does not fit the job requirements")], limit=1)

    for data in APPLICANTS:
        env["hr.applicant"].create({
            "partner_name": data["partner_name"],
            "email_from": data["email_from"],
            "job_id": job.id,
            "active": True,
        })
