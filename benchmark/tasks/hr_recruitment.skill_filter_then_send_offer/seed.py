"""Seed data for hr_recruitment.skill_filter_then_send_offer.

Category 2 (HARD): the agent must apply a non-default custom Skills
search-filter on Recruitment → Applications, then among several
matching applicants pick the only one who is simultaneously
  (a) applied to the QA Lead job position, AND
  (b) tagged Senior.
Then from the cog Actions menu launch the Send Email wizard and fill
BOTH the subject AND the body with an exact offer text.

Hard patterns combined:
  1. Custom m2m search-filter selection from autocomplete
     ("Skills" entry — not "Applicant", "Tag", "Stage").
  2. Among 4 Python-skilled matches, pick the one that is BOTH senior
     AND on the QA Lead job (other three are on different jobs or are
     Junior/Contractor).
  3. Send-email wizard with exact subject AND body override
     (date string inside body — BU tends to leave body empty).
"""

JOB_QA_LEAD = "QA Lead"
JOB_SENIOR_DEV = "Senior Backend Developer"
DEPARTMENT_QA = "Quality Assurance"
DEPARTMENT_ENG = "Engineering"

ALICE_NAME = "Alice Senior"          # CORRECT target
BOB_NAME = "Bob Junior"              # same job, wrong tag
DANA_NAME = "Dana Pirate"            # Senior tag, wrong job
EVE_NAME = "Eve Contractor"          # same job, wrong tag
CHARLIE_NAME = "Charlie Jones"       # distractor, no Python

ALICE_EMAIL = "alice.senior@example.com"
BOB_EMAIL = "bob.junior@example.com"
DANA_EMAIL = "dana.pirate@example.com"
EVE_EMAIL = "eve.contractor@example.com"
CHARLIE_EMAIL = "charlie.jones@example.com"

SKILL_TYPE = "Programming Languages"
PYTHON_SKILL = "Python"
JS_SKILL = "JavaScript"

TAG_SENIOR = "Senior"
TAG_JUNIOR = "Junior"
TAG_CONTRACTOR = "Contractor"
TAG_NEW = "New"

OFFER_SUBJECT = "Job Offer - QA Lead"
OFFER_BODY_MARKER = "2026-06-01"  # start date the agent must type in body


def _ensure_module(env, name):
    mod = env["ir.module.module"].sudo().search([("name", "=", name)], limit=1)
    if mod and mod.state != "installed":
        mod.button_immediate_install()


def _ensure_skill_type(env, name):
    rec = env["hr.skill.type"].search([("name", "=", name)], limit=1)
    if not rec:
        rec = env["hr.skill.type"].create({"name": name})
    return rec


def _ensure_skill(env, skill_type, name):
    rec = env["hr.skill"].search([
        ("name", "=", name),
        ("skill_type_id", "=", skill_type.id),
    ], limit=1)
    if not rec:
        rec = env["hr.skill"].create({
            "name": name,
            "skill_type_id": skill_type.id,
        })
    return rec


def _ensure_level(env, skill_type, name, progress):
    rec = env["hr.skill.level"].search([
        ("name", "=", name),
        ("skill_type_id", "=", skill_type.id),
    ], limit=1)
    if not rec:
        rec = env["hr.skill.level"].create({
            "name": name,
            "skill_type_id": skill_type.id,
            "level_progress": progress,
        })
    return rec


def _ensure_tag(env, name):
    rec = env["hr.applicant.category"].search([("name", "=", name)], limit=1)
    if not rec:
        rec = env["hr.applicant.category"].create({"name": name})
    return rec


def _ensure_department(env, name):
    rec = env["hr.department"].search([("name", "=", name)], limit=1)
    if not rec:
        rec = env["hr.department"].create({"name": name})
    return rec


def _ensure_job(env, name, dept):
    rec = env["hr.job"].search([("name", "=", name)], limit=1)
    if not rec:
        rec = env["hr.job"].create({
            "name": name,
            "department_id": dept.id,
            "no_of_recruitment": 1,
        })
    else:
        rec.write({"department_id": dept.id})
    return rec


def _ensure_stage(env, job, name, sequence):
    stage = env["hr.recruitment.stage"].search([
        ("name", "=", name),
    ], limit=1)
    if not stage:
        stage = env["hr.recruitment.stage"].create({
            "name": name,
            "sequence": sequence,
        })
    if job not in stage.job_ids:
        stage.write({"job_ids": [(4, job.id)]})
    return stage


def setup(env):
    # 0. Ensure skills modules are installed
    _ensure_module(env, "hr_skills")
    _ensure_module(env, "hr_recruitment_skills")

    # 1. Cleanup prior runs (also purge their chatter messages)
    names = [ALICE_NAME, BOB_NAME, DANA_NAME, EVE_NAME, CHARLIE_NAME]
    old = env["hr.applicant"].with_context(active_test=False).search([
        ("partner_name", "in", names),
    ])
    for app in old:
        app.applicant_skill_ids.unlink()
        env["mail.message"].sudo().search([
            ("model", "=", "hr.applicant"),
            ("res_id", "=", app.id),
        ]).unlink()
    old.unlink()

    # 2. Departments + jobs
    dept_qa = _ensure_department(env, DEPARTMENT_QA)
    dept_eng = _ensure_department(env, DEPARTMENT_ENG)
    job_qa = _ensure_job(env, JOB_QA_LEAD, dept_qa)
    job_dev = _ensure_job(env, JOB_SENIOR_DEV, dept_eng)

    # 3. Stages for each job
    _ensure_stage(env, job_qa, "Initial Qualification", 10)
    _ensure_stage(env, job_dev, "Initial Qualification", 10)
    init_qa = env["hr.recruitment.stage"].search([
        ("name", "=", "Initial Qualification"),
        ("job_ids", "in", [job_qa.id]),
    ], limit=1)
    init_dev = env["hr.recruitment.stage"].search([
        ("name", "=", "Initial Qualification"),
        ("job_ids", "in", [job_dev.id]),
    ], limit=1)

    # 4. Skill type, skills, levels
    skill_type = _ensure_skill_type(env, SKILL_TYPE)
    python_skill = _ensure_skill(env, skill_type, PYTHON_SKILL)
    js_skill = _ensure_skill(env, skill_type, JS_SKILL)
    level_beginner = _ensure_level(env, skill_type, "Beginner", 25)
    level_intermediate = _ensure_level(env, skill_type, "Intermediate", 50)
    level_advanced = _ensure_level(env, skill_type, "Advanced", 75)
    level_expert = _ensure_level(env, skill_type, "Expert", 100)

    # 5. Tags
    tag_senior = _ensure_tag(env, TAG_SENIOR)
    tag_junior = _ensure_tag(env, TAG_JUNIOR)
    tag_contractor = _ensure_tag(env, TAG_CONTRACTOR)
    tag_new = _ensure_tag(env, TAG_NEW)

    # 6. Seed five applicants
    # 6a. Alice Senior — CORRECT: QA Lead + Senior + Python Expert
    env["hr.applicant"].create({
        "partner_name": ALICE_NAME,
        "email_from": ALICE_EMAIL,
        "partner_phone": "+1 555 0101",
        "job_id": job_qa.id,
        "stage_id": init_qa.id,
        "priority": "0",
        "categ_ids": [(6, 0, [tag_senior.id])],
        "applicant_skill_ids": [(0, 0, {
            "skill_id": python_skill.id,
            "skill_type_id": skill_type.id,
            "skill_level_id": level_expert.id,
        })],
    })

    # 6b. Bob Junior — same job, Junior tag
    env["hr.applicant"].create({
        "partner_name": BOB_NAME,
        "email_from": BOB_EMAIL,
        "partner_phone": "+1 555 0202",
        "job_id": job_qa.id,
        "stage_id": init_qa.id,
        "priority": "0",
        "categ_ids": [(6, 0, [tag_junior.id])],
        "applicant_skill_ids": [(0, 0, {
            "skill_id": python_skill.id,
            "skill_type_id": skill_type.id,
            "skill_level_id": level_beginner.id,
        })],
    })

    # 6c. Dana Pirate — Senior tag but WRONG job (Senior Backend Developer)
    env["hr.applicant"].create({
        "partner_name": DANA_NAME,
        "email_from": DANA_EMAIL,
        "partner_phone": "+1 555 0303",
        "job_id": job_dev.id,
        "stage_id": init_dev.id,
        "priority": "0",
        "categ_ids": [(6, 0, [tag_senior.id])],
        "applicant_skill_ids": [(0, 0, {
            "skill_id": python_skill.id,
            "skill_type_id": skill_type.id,
            "skill_level_id": level_advanced.id,
        })],
    })

    # 6d. Eve Contractor — QA Lead, but Contractor tag (not Senior)
    env["hr.applicant"].create({
        "partner_name": EVE_NAME,
        "email_from": EVE_EMAIL,
        "partner_phone": "+1 555 0404",
        "job_id": job_qa.id,
        "stage_id": init_qa.id,
        "priority": "0",
        "categ_ids": [(6, 0, [tag_contractor.id])],
        "applicant_skill_ids": [(0, 0, {
            "skill_id": python_skill.id,
            "skill_type_id": skill_type.id,
            "skill_level_id": level_intermediate.id,
        })],
    })

    # 6e. Charlie Jones — distractor: no Python skill
    env["hr.applicant"].create({
        "partner_name": CHARLIE_NAME,
        "email_from": CHARLIE_EMAIL,
        "partner_phone": "+1 555 0505",
        "job_id": job_qa.id,
        "stage_id": init_qa.id,
        "priority": "0",
        "categ_ids": [(6, 0, [tag_new.id])],
        "applicant_skill_ids": [(0, 0, {
            "skill_id": js_skill.id,
            "skill_type_id": skill_type.id,
            "skill_level_id": level_intermediate.id,
        })],
    })

    env.cr.commit()
