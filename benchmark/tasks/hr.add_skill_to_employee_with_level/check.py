"""Postcondition checks for hr.add_skill_to_employee_with_level."""


EMPLOYEE_NAME = "Tech Tom"
SKILL_TYPE_NAME = "Programming Languages"
SKILL_NAME = "Python"
SKILL_LEVEL_NAME = "Advanced"


def check(env):
    failures = []

    employee = env["hr.employee"].search([("name", "=", EMPLOYEE_NAME)], limit=1)
    if not employee:
        return [f"Employee '{EMPLOYEE_NAME}' not found"]

    skills = employee.employee_skill_ids
    if not skills:
        failures.append(f"No skills found for '{EMPLOYEE_NAME}'")
        return failures

    matching = skills.filtered(lambda s: s.skill_id.name == SKILL_NAME)
    if not matching:
        skill_names = skills.mapped("skill_id.name")
        failures.append(
            f"Skill '{SKILL_NAME}' not found. Found skills: {skill_names}"
        )
        return failures

    skill_entry = matching[0]

    if skill_entry.skill_type_id.name != SKILL_TYPE_NAME:
        failures.append(
            f"Skill type is '{skill_entry.skill_type_id.name}', expected '{SKILL_TYPE_NAME}'"
        )

    if skill_entry.skill_level_id.name != SKILL_LEVEL_NAME:
        failures.append(
            f"Skill level is '{skill_entry.skill_level_id.name}', expected '{SKILL_LEVEL_NAME}'"
        )

    # Ensure no unexpected skills were added for Tom
    if len(skills) > 1:
        extra = [s.skill_id.name for s in skills if s.skill_id.name != SKILL_NAME]
        failures.append(
            f"Expected 1 skill, found {len(skills)}. Extra skills: {extra}"
        )

    return failures
