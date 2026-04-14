"""Seed a job position with a demo user for activity assignment.

Category 5: Deep UI interaction.
The agent must create a new applicant from scratch (filling exact fields)
and then schedule an activity via the chatter popover with a specific date,
assignee, and summary.  Browser-use struggles with: (a) create-from-scratch
forms (phantom empty records), and (b) chatter activity popovers that contain
date pickers and Many2one autocomplete fields.
"""


def setup(env):
    # ------------------------------------------------------------------
    # 1. Cleanup prior runs
    # ------------------------------------------------------------------
    old_applicants = env["hr.applicant"].search([
        ("partner_name", "=", "Elena Vasquez"),
    ])
    if old_applicants:
        # Cancel any linked activities first
        env["mail.activity"].search([
            ("res_model", "=", "hr.applicant"),
            ("res_id", "in", old_applicants.ids),
        ]).unlink()
        old_applicants.unlink()

    # ------------------------------------------------------------------
    # 2. Ensure Development department exists
    # ------------------------------------------------------------------
    dept = env["hr.department"].search([("name", "=", "Development")], limit=1)
    if not dept:
        dept = env["hr.department"].create({"name": "Development"})

    # ------------------------------------------------------------------
    # 3. Ensure Marc Demo user exists (for activity assignment)
    # ------------------------------------------------------------------
    marc_user = env["res.users"].search([("login", "=", "marc.demo")], limit=1)
    if not marc_user:
        marc_user = env["res.users"].create({
            "name": "Marc Demo",
            "login": "marc.demo",
            "password": "marc.demo",
            "group_ids": [(4, env.ref("hr_recruitment.group_hr_recruitment_user").id)],
        })

    # ------------------------------------------------------------------
    # 4. Ensure job position exists
    # ------------------------------------------------------------------
    job = env["hr.job"].search([("name", "=", "Senior Backend Developer")], limit=1)
    if not job:
        job = env["hr.job"].create({
            "name": "Senior Backend Developer",
            "department_id": dept.id,
            "no_of_recruitment": 2,
        })
    else:
        job.write({
            "department_id": dept.id,
            "no_of_recruitment": 2,
        })

    # ------------------------------------------------------------------
    # 5. Create a distractor applicant (must not be modified)
    # ------------------------------------------------------------------
    distractor = env["hr.applicant"].search([
        ("partner_name", "=", "Alex Kemp"),
        ("job_id", "=", job.id),
    ], limit=1)
    if not distractor:
        qualification_stage = env["hr.recruitment.stage"].search([
            ("name", "ilike", "Qualification"),
        ], limit=1)
        env["hr.applicant"].create({
            "partner_name": "Alex Kemp",
            "email_from": "alex.kemp@example.com",
            "partner_phone": "+1 555-0199",
            "job_id": job.id,
            "department_id": dept.id,
            "user_id": marc_user.id,
            "stage_id": qualification_stage.id if qualification_stage else False,
            "salary_expected": 78000,
        })
