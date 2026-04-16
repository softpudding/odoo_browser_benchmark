"""Seed data for hr_recruitment.schedule_interview_for_applicant."""

JOB_NAME = "Operations Analyst"
TARGET_NAME = "Riley Mercer"
DISTRACTOR_NAME = "Riley Mercer West"
SUMMARY = "Schedule first interview"


def setup(env):
    applicants = env["hr.applicant"].search([
        ("partner_name", "in", [TARGET_NAME, DISTRACTOR_NAME]),
    ])
    if applicants:
        env["mail.activity"].search([
            ("res_model", "=", "hr.applicant"),
            ("res_id", "in", applicants.ids),
        ]).unlink()
        applicants.unlink()

    env["mail.activity"].search([("summary", "=", SUMMARY)]).unlink()

    dept = env["hr.department"].search([("name", "=", "Operations")], limit=1)
    if not dept:
        dept = env["hr.department"].create({"name": "Operations"})

    job = env["hr.job"].search([("name", "=", JOB_NAME)], limit=1)
    if not job:
        job = env["hr.job"].create({
            "name": JOB_NAME,
            "department_id": dept.id,
            "no_of_recruitment": 1,
        })

    stage = env["hr.recruitment.stage"].search([("name", "=", "Initial Qualification")], limit=1)
    if not stage:
        stage = env["hr.recruitment.stage"].create({
            "name": "Initial Qualification",
            "sequence": 10,
            "job_ids": [(4, job.id)],
        })
    elif job not in stage.job_ids:
        stage.write({"job_ids": [(4, job.id)]})

    for name in [TARGET_NAME, DISTRACTOR_NAME]:
        env["hr.applicant"].create({
            "partner_name": name,
            "email_from": f"{name.lower().replace(' ', '.')}@example.com",
            "job_id": job.id,
            "department_id": dept.id,
            "stage_id": stage.id,
        })
