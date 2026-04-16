"""Seed an employee and skill data for the add_employee_skill task.

Category 2 (MEDIUM): Navigate to the employee's Resume tab and add a structured
skill entry — selecting a skill type, skill name, and proficiency level from a
skill matrix table. This tests inline record creation within the skill widget.
"""

EMPLOYEE_NAME = "Priya Mehta"
SKILL_TYPE_NAME = "IT Skills"
SKILL_NAME = "Python"
SKILL_LEVEL_NAME = "Advanced"


def _cleanup(env):
    employee = env["hr.employee"].search([("name", "=", EMPLOYEE_NAME)])
    for emp in employee:
        emp.employee_skill_ids.unlink()
        emp.unlink()


def _ensure_skill_type(env, name):
    skill_type = env["hr.skill.type"].search([("name", "=", name)], limit=1)
    if not skill_type:
        skill_type = env["hr.skill.type"].create({"name": name})
    return skill_type


def _ensure_skill(env, skill_type, name):
    skill = env["hr.skill"].search([
        ("skill_type_id", "=", skill_type.id),
        ("name", "=", name),
    ], limit=1)
    if not skill:
        skill = env["hr.skill"].create({
            "skill_type_id": skill_type.id,
            "name": name,
        })
    return skill


def _ensure_skill_level(env, skill_type, name, progress):
    level = env["hr.skill.level"].search([
        ("skill_type_id", "=", skill_type.id),
        ("name", "=", name),
    ], limit=1)
    if not level:
        level = env["hr.skill.level"].create({
            "skill_type_id": skill_type.id,
            "name": name,
            "progress": progress,
        })
    return level


def setup(env):
    _cleanup(env)

    # Ensure skill type, skill, and levels exist
    skill_type = _ensure_skill_type(env, SKILL_TYPE_NAME)
    _ensure_skill(env, skill_type, SKILL_NAME)
    _ensure_skill_level(env, skill_type, "Beginner", 25)
    _ensure_skill_level(env, skill_type, "Intermediate", 50)
    _ensure_skill_level(env, skill_type, SKILL_LEVEL_NAME, 75)
    _ensure_skill_level(env, skill_type, "Expert", 100)

    # Create the target employee (no skills yet — agent adds them)
    job_position = env["hr.job"].search([("name", "ilike", "analyst")], limit=1)
    env["hr.employee"].create({
        "name": EMPLOYEE_NAME,
        "job_id": job_position.id if job_position else False,
        "job_title": "Data Analyst",
    })
