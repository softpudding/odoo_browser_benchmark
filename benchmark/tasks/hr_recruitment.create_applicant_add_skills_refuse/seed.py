"""Seed data for hr_recruitment.create_applicant_add_skills_refuse.

Category 3 (HARD): The agent must create a new applicant with full details,
add a skill through the cascading skill widget (skill type -> skill -> level),
then refuse the applicant via the refuse wizard with a non-default reason and
unchecked send-email option.
"""

JOB_NAME = "Senior Data Engineer"
APPLICANT_NAME = "Cameron Blake"
DISTRACTOR_NAME = "Cameron Brooks"
SKILL_TYPE = "Languages"
SKILL_NAME = "Python"
SKILL_LEVEL = "Advanced"
REFUSE_REASON = "Does not fit the job requirements"


def _ensure_skill_type(env, name):
    skill_type = env["hr.skill.type"].search([("name", "=", name)], limit=1)
    if not skill_type:
        skill_type = env["hr.skill.type"].create({"name": name})
    return skill_type


def _ensure_skill(env, skill_type, name):
    skill = env["hr.skill"].search([
        ("name", "=", name),
        ("skill_type_id", "=", skill_type.id),
    ], limit=1)
    if not skill:
        skill = env["hr.skill"].create({
            "name": name,
            "skill_type_id": skill_type.id,
        })
    return skill


def _ensure_skill_level(env, skill_type, name, progress):
    level = env["hr.skill.level"].search([
        ("name", "=", name),
        ("skill_type_id", "=", skill_type.id),
    ], limit=1)
    if not level:
        level = env["hr.skill.level"].create({
            "name": name,
            "skill_type_id": skill_type.id,
            "level_progress": progress,
        })
    return level


def setup(env):
    # Clean up prior runs
    old_applicants = env["hr.applicant"].with_context(active_test=False).search([
        ("partner_name", "in", [APPLICANT_NAME, DISTRACTOR_NAME]),
    ])
    for app in old_applicants:
        app.applicant_skill_ids.unlink()
        env["mail.message"].search([
            ("model", "=", "hr.applicant"),
            ("res_id", "=", app.id),
        ]).unlink()
    old_applicants.unlink()

    # Ensure department
    department = env["hr.department"].search([("name", "=", "IT Department")], limit=1)
    if not department:
        department = env["hr.department"].create({"name": "IT Department"})

    # Ensure job position
    job = env["hr.job"].search([("name", "=", JOB_NAME)], limit=1)
    if not job:
        job = env["hr.job"].create({
            "name": JOB_NAME,
            "department_id": department.id,
            "no_of_recruitment": 3,
        })

    # Make sure job is in recruit state
    if hasattr(job, "state") and job.state != "recruit":
        try:
            job.set_recruit()
        except Exception:
            pass

    # Ensure skill type with skill and levels
    skill_type = _ensure_skill_type(env, SKILL_TYPE)
    _ensure_skill(env, skill_type, SKILL_NAME)
    # Also add a distractor skill
    _ensure_skill(env, skill_type, "Java")
    _ensure_skill_level(env, skill_type, "Beginner", 25)
    _ensure_skill_level(env, skill_type, "Intermediate", 50)
    _ensure_skill_level(env, skill_type, SKILL_LEVEL, 75)
    _ensure_skill_level(env, skill_type, "Expert", 100)

    # Ensure refuse reason exists (it is standard data, but be safe)
    refuse_reason = env["hr.applicant.refuse.reason"].search([
        ("name", "=", REFUSE_REASON),
    ], limit=1)
    if not refuse_reason:
        env["hr.applicant.refuse.reason"].create({
            "name": REFUSE_REASON,
            "sequence": 12,
        })

    # Create distractor applicant on the same job
    env["hr.applicant"].create({
        "partner_name": DISTRACTOR_NAME,
        "email_from": "cameron.brooks@techmail.example.com",
        "partner_phone": "+1 555 0199",
        "job_id": job.id,
        "active": True,
    })
