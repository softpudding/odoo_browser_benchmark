"""Seed an applicant for the add-skill-move-stage task.

Category 2 (MEDIUM): the agent must find the right applicant under the correct
job, update the stage, and add one skill through the applicant skills widget.
"""

JOB_NAME = "Backend Platform Engineer"
APPLICANT_NAME = "Jordan Park"
SKILL_TYPE = "IT Skills"
SKILL_NAME = "Python"
SKILL_LEVEL = "Advanced"


def _ensure_stage(env, job, name, sequence):
    stage = env["hr.recruitment.stage"].search([
        ("name", "=", name),
        ("job_ids", "in", [job.id]),
    ], limit=1)
    if stage:
        return stage

    global_stage = env["hr.recruitment.stage"].search([("name", "=", name)], limit=1)
    if global_stage:
        if job not in global_stage.job_ids:
            global_stage.write({"job_ids": [(4, job.id)]})
        return global_stage

    return env["hr.recruitment.stage"].create({
        "name": name,
        "sequence": sequence,
        "job_ids": [(4, job.id)],
    })


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
    applicants = env["hr.applicant"].search([("partner_name", "=", APPLICANT_NAME)])
    applicants.applicant_skill_ids.unlink()
    applicants.unlink()

    department = env["hr.department"].search([("name", "=", "Engineering")], limit=1)
    if not department:
        department = env["hr.department"].create({"name": "Engineering"})

    job = env["hr.job"].search([("name", "=", JOB_NAME)], limit=1)
    if not job:
        job = env["hr.job"].create({
            "name": JOB_NAME,
            "department_id": department.id,
            "no_of_recruitment": 1,
        })

    initial = _ensure_stage(env, job, "Initial Qualification", 10)
    _ensure_stage(env, job, "First Interview", 20)
    _ensure_stage(env, job, "Second Interview", 30)

    skill_type = _ensure_skill_type(env, SKILL_TYPE)
    _ensure_skill(env, skill_type, SKILL_NAME)
    _ensure_skill_level(env, skill_type, "Beginner", 25)
    _ensure_skill_level(env, skill_type, "Intermediate", 50)
    _ensure_skill_level(env, skill_type, SKILL_LEVEL, 75)

    env["hr.applicant"].create({
        "partner_name": APPLICANT_NAME,
        "email_from": "jordan.park@example.com",
        "partner_phone": "+1 415 555 0175",
        "job_id": job.id,
        "stage_id": initial.id,
        "priority": "0",
    })
