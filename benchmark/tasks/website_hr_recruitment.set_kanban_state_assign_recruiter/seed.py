"""Seed an applicant + a Recruiter Bob user for the kanban-state task.

Category 5 (MEDIUM): Open an existing applicant 'Diana Recruit' linked to job
'Senior QA Engineer', flip the kanban_state status ball to 'Ready for Next
Stage', set the Recruiter many2one to 'Recruiter Bob', and post an internal
Log note ('Phone screen done.') in the chatter.

The kanban_state widget is a small colored ball next to the applicant name.
Browser-use frequently misses it. The internal Log-note vs Send-message
distinction is also a known failure mode.
"""

JOB_NAME = "Senior QA Engineer"
APPLICANT_NAME = "Diana Recruit"
RECRUITER_LOGIN = "recruiter.bob"
RECRUITER_NAME = "Recruiter Bob"


def setup(env):
    # ------------------------------------------------------------------
    # 1. Cleanup prior runs (applicants first to release follower refs)
    # ------------------------------------------------------------------
    old_apps = env["hr.applicant"].with_context(active_test=False).search([
        ("partner_name", "=", APPLICANT_NAME),
    ])
    if old_apps:
        # Drop any chatter messages and activities first
        env["mail.message"].search([
            ("model", "=", "hr.applicant"),
            ("res_id", "in", old_apps.ids),
        ]).sudo().unlink()
        env["mail.activity"].search([
            ("res_model", "=", "hr.applicant"),
            ("res_id", "in", old_apps.ids),
        ]).sudo().unlink()
        old_apps.sudo().unlink()

    # ------------------------------------------------------------------
    # 2. Ensure the QA department exists
    # ------------------------------------------------------------------
    dept = env["hr.department"].search([("name", "=", "Quality Assurance")], limit=1)
    if not dept:
        dept = env["hr.department"].create({"name": "Quality Assurance"})

    # ------------------------------------------------------------------
    # 3. Ensure the Recruiter Bob user exists with recruitment access
    # ------------------------------------------------------------------
    bob = env["res.users"].search([("login", "=", RECRUITER_LOGIN)], limit=1)
    if not bob:
        bob = env["res.users"].create({
            "name": RECRUITER_NAME,
            "login": RECRUITER_LOGIN,
            "password": RECRUITER_LOGIN,
            "group_ids": [
                (4, env.ref("hr_recruitment.group_hr_recruitment_user").id),
            ],
        })
    elif bob.name != RECRUITER_NAME:
        bob.sudo().write({"name": RECRUITER_NAME})

    # ------------------------------------------------------------------
    # 4. Ensure job position exists (linked to the QA department)
    # ------------------------------------------------------------------
    job = env["hr.job"].search([("name", "=", JOB_NAME)], limit=1)
    if not job:
        job = env["hr.job"].create({
            "name": JOB_NAME,
            "department_id": dept.id,
            "no_of_recruitment": 1,
        })
    else:
        job.write({
            "department_id": dept.id,
            "no_of_recruitment": 1,
        })

    # ------------------------------------------------------------------
    # 5. Find/create an "Initial Qualification" stage linked to the job
    # ------------------------------------------------------------------
    stage = env["hr.recruitment.stage"].search(
        [("name", "=", "Initial Qualification")], limit=1
    )
    if not stage:
        stage = env["hr.recruitment.stage"].create({
            "name": "Initial Qualification",
            "sequence": 5,
            "job_ids": [(4, job.id)],
        })
    elif job not in stage.job_ids:
        stage.write({"job_ids": [(4, job.id)]})

    # ------------------------------------------------------------------
    # 6. Create the applicant in 'normal' kanban_state with NO recruiter
    # ------------------------------------------------------------------
    env["hr.applicant"].create({
        "partner_name": APPLICANT_NAME,
        "email_from": "diana.recruit@example.com",
        "partner_phone": "+1 555-0177",
        "job_id": job.id,
        "department_id": dept.id,
        "stage_id": stage.id,
        "kanban_state": "normal",
        "user_id": False,  # task asks the agent to set the Recruiter
        "priority": "0",
    })
