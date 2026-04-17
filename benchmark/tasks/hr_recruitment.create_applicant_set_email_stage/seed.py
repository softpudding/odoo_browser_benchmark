"""Seed an applicant for the advance-applicant-stage task.

Category 2 (MEDIUM): Navigate to a job position, find an applicant in
the kanban, move to the next stage, set appreciation, and write a summary.
Multi-step within recruitment module with kanban + form interaction.
"""

JOB_NAME = "Experienced Developer"
APPLICANT_NAME = "Taylor Kim"


def setup(env):
    # --- Cleanup prior runs ---
    old_apps = env["hr.applicant"].search([
        ("partner_name", "=", APPLICANT_NAME),
    ])
    old_apps.unlink()

    # --- Ensure job position exists ---
    job = env["hr.job"].search([("name", "=", JOB_NAME)], limit=1)
    if not job:
        dept = env["hr.department"].search(
            [("name", "=", "Engineering")], limit=1
        )
        if not dept:
            dept = env["hr.department"].create({"name": "Engineering"})
        job = env["hr.job"].create({
            "name": JOB_NAME,
            "department_id": dept.id,
            "no_of_recruitment": 2,
        })

    # --- Ensure stages exist ---
    stage_names = ["Initial Qualification", "First Interview", "Second Interview", "Contract Proposal"]
    for idx, sname in enumerate(stage_names):
        stage = env["hr.recruitment.stage"].search(
            [("name", "=", sname)], limit=1
        )
        if not stage:
            env["hr.recruitment.stage"].create({
                "name": sname,
                "sequence": (idx + 1) * 10,
                "job_ids": [(4, job.id)],
            })
        else:
            # Make sure it's linked to this job
            if job not in stage.job_ids:
                stage.write({"job_ids": [(4, job.id)]})

    initial_stage = env["hr.recruitment.stage"].search(
        [("name", "=", "Initial Qualification")], limit=1
    )

    # --- Create the applicant ---
    env["hr.applicant"].create({
        "partner_name": APPLICANT_NAME,
        "email_from": "taylor.kim@email.com",
        "partner_phone": "+1 555 0400",
        "job_id": job.id,
        "stage_id": initial_stage.id,
        "priority": "0",  # Normal (no stars)
    })
