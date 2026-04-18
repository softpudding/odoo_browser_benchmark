"""Seed for hr.add_skill_to_employee_with_level.

Category 5 (MEDIUM): deep UI interaction with cascading dropdowns.

The agent must open employee 'Tech Tom' and add a skill row where three fields
cascade: Skill Type -> Skill -> Level. Setting Skill Type first is required
before the Skill list becomes usable, and Level is filtered by Skill Type too.

We seed a fresh skill type 'Programming Languages' (distinct from the 'IT Skills'
type used by hr.add_employee_skill) so entity keys don't collide with that task.
We do NOT pre-create any hr.employee.skill row for Tom — the agent must create it.
"""

EMPLOYEE_NAME = "Tech Tom"
SKILL_TYPE_NAME = "Programming Languages"
SKILL_NAME = "Python"
SKILL_LEVEL_NAME = "Advanced"


def _ensure_hr_skills_installed(env):
    """Install hr_skills on demand if not present. The reference task
    hr.add_employee_skill assumes it is installed; to be safe we install it."""
    mod = env["ir.module.module"].search([("name", "=", "hr_skills")], limit=1)
    if mod and mod.state != "installed":
        mod.button_immediate_install()


def _cleanup(env):
    # Remove prior Tech Tom and any skill rows
    employees = env["hr.employee"].with_context(active_test=False).search(
        [("name", "=", EMPLOYEE_NAME)]
    )
    for emp in employees:
        emp.employee_skill_ids.unlink()
        emp.sudo().unlink()


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
            "level_progress": progress,
        })
    return level


def setup(env):
    _ensure_hr_skills_installed(env)
    _cleanup(env)

    # Ensure skill type 'Programming Languages' with a couple of languages
    skill_type = _ensure_skill_type(env, SKILL_TYPE_NAME)
    _ensure_skill(env, skill_type, "Python")
    _ensure_skill(env, skill_type, "JavaScript")
    _ensure_skill(env, skill_type, "Go")

    # Ensure levels exist for the skill type
    _ensure_skill_level(env, skill_type, "Beginner", 25)
    _ensure_skill_level(env, skill_type, "Intermediate", 50)
    _ensure_skill_level(env, skill_type, SKILL_LEVEL_NAME, 75)
    _ensure_skill_level(env, skill_type, "Expert", 100)

    # Create Tech Tom with no skills — the agent adds them
    job_position = env["hr.job"].search([("name", "ilike", "developer")], limit=1)
    env["hr.employee"].create({
        "name": EMPLOYEE_NAME,
        "job_id": job_position.id if job_position else False,
        "job_title": "Software Developer",
    })
