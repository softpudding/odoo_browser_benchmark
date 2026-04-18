"""Seed for hr_recruitment_survey.attach_survey_require_applicant_submit.

Installs the hr_recruitment_survey bridge module on demand, then seeds:
  - A 'Bench Screening' survey.survey with survey_type='recruitment' and
    one page + two questions.
  - An hr.job 'Bench Recruit Lead' with NO survey attached (the agent
    must pick it).
  - An hr.applicant 'Alice Candidate' linked to that job.

The domain on hr.job.survey_id is [('survey_type','=','recruitment')]
so the survey MUST carry that type — otherwise the autocomplete shows
nothing and the task is unsolvable.

The Recruitment tab on the hr.job form has groups gated by
`hr_recruitment.group_hr_recruitment_interviewer` / `hr.group_hr_user`
— the admin user already has these in the base snapshot, but we
idempotently ensure the group for safety.
"""

SURVEY_TITLE = "Bench Screening"
JOB_NAME = "Bench Recruit Lead"
APPLICANT_NAME = "Alice Candidate"


def _ensure_module(env, name):
    mod = env["ir.module.module"].search([("name", "=", name)], limit=1)
    if mod and mod.state != "installed":
        mod.button_immediate_install()


def setup(env):
    # Ensure required modules are installed.
    _ensure_module(env, "survey")
    _ensure_module(env, "hr_recruitment_survey")

    # Make sure admin has the recruitment interviewer group so the
    # Recruitment tab renders (it is gated by that group in the inherited view).
    admin = env.ref("base.user_admin")
    for xmlid in (
        "hr_recruitment.group_hr_recruitment_interviewer",
        "hr.group_hr_user",
    ):
        grp = env.ref(xmlid, raise_if_not_found=False)
        if grp and admin not in grp.user_ids:
            grp.user_ids = [(4, admin.id)]

    # --- Cleanup prior runs (child-first) ---
    env["hr.applicant"].with_context(active_test=False).search([
        ("partner_name", "=", APPLICANT_NAME),
    ]).unlink()

    old_jobs = env["hr.job"].with_context(active_test=False).search([
        ("name", "=", JOB_NAME),
    ])
    # Decouple any prior survey before unlinking
    if old_jobs:
        old_jobs.write({"survey_id": False})
        old_jobs.unlink()

    old_surveys = env["survey.survey"].with_context(active_test=False).search([
        ("title", "=", SURVEY_TITLE),
    ])
    if old_surveys:
        old_surveys.question_and_page_ids.unlink()
        old_surveys.unlink()

    # --- Create the survey with type='recruitment' (required by domain) ---
    survey = env["survey.survey"].create({
        "title": SURVEY_TITLE,
        "survey_type": "recruitment",
        "access_mode": "token",
        "questions_layout": "one_page",
    })

    # Add 1 page + 2 simple questions.
    env["survey.question"].create([
        {
            "survey_id": survey.id,
            "title": "Background",
            "sequence": 10,
            "is_page": True,
            "questions_selection": "all",
        },
        {
            "survey_id": survey.id,
            "title": "Describe your most relevant experience",
            "sequence": 20,
            "question_type": "text_box",
        },
        {
            "survey_id": survey.id,
            "title": "How many years of experience?",
            "sequence": 30,
            "question_type": "numerical_box",
        },
    ])

    # --- Create the job WITHOUT a survey attached ---
    dept = env["hr.department"].search([("name", "=", "Bench HR")], limit=1)
    if not dept:
        dept = env["hr.department"].create({"name": "Bench HR"})

    job = env["hr.job"].create({
        "name": JOB_NAME,
        "department_id": dept.id,
        "no_of_recruitment": 1,
    })

    # Ensure at least one stage is linked so applicant kanban renders.
    initial_stage = env["hr.recruitment.stage"].search(
        [("name", "=", "Initial Qualification")], limit=1
    )
    if not initial_stage:
        initial_stage = env["hr.recruitment.stage"].create({
            "name": "Initial Qualification",
            "sequence": 1,
            "job_ids": [(4, job.id)],
        })
    elif job not in initial_stage.job_ids:
        initial_stage.write({"job_ids": [(4, job.id)]})

    # --- Create the applicant ---
    env["hr.applicant"].create({
        "partner_name": APPLICANT_NAME,
        "email_from": "alice.candidate@example.com",
        "partner_phone": "+1 555 0920",
        "job_id": job.id,
        "stage_id": initial_stage.id,
    })
