"""Seed for hr_recruitment.schedule_second_interview_with_feedback."""


TARGET_NAME = "Mina Chen"
DISTRACTOR_NAME = "Mina Chen West"


def setup(env):
    applicants = env["hr.applicant"].search([
        ("partner_name", "in", [TARGET_NAME, DISTRACTOR_NAME]),
    ])
    if applicants:
        env["calendar.event"].search([("applicant_id", "in", applicants.ids)]).unlink()
        applicants.unlink()

    dept = env["hr.department"].search([("name", "=", "Operations")], limit=1)
    if not dept:
        dept = env["hr.department"].create({"name": "Operations"})

    job = env["hr.job"].search([("name", "=", "Dock Supervisor")], limit=1)
    if not job:
        job = env["hr.job"].create({
            "name": "Dock Supervisor",
            "department_id": dept.id,
            "no_of_recruitment": 1,
        })

    first_stage = env["hr.recruitment.stage"].search([("name", "=", "First Interview")], limit=1)
    if not first_stage:
        raise RuntimeError("Missing recruitment stage 'First Interview'")
    if job not in first_stage.job_ids:
        first_stage.write({"job_ids": [(4, job.id)]})

    second_stage = env["hr.recruitment.stage"].search([("name", "=", "Second Interview")], limit=1)
    if not second_stage:
        raise RuntimeError("Missing recruitment stage 'Second Interview'")
    if job not in second_stage.job_ids:
        second_stage.write({"job_ids": [(4, job.id)]})

    for name in [TARGET_NAME, DISTRACTOR_NAME]:
        env["hr.applicant"].create({
            "partner_name": name,
            "email_from": f"{name.lower().replace(' ', '.')}@example.com",
            "partner_phone": "+1 555-0110" if name == TARGET_NAME else "+1 555-0111",
            "job_id": job.id,
            "department_id": dept.id,
            "stage_id": first_stage.id,
        })
