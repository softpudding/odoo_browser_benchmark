"""Postcondition checks for hr_recruitment.add_skill_move_stage."""


APPLICANT_NAME = "Jordan Park"


def check(env):
    failures = []

    applicant = env["hr.applicant"].search([
        ("partner_name", "=", APPLICANT_NAME),
    ], limit=1)
    if not applicant:
        return [f"Applicant '{APPLICANT_NAME}' not found"]

    if applicant.stage_id.name != "First Interview":
        failures.append(
            f"Applicant stage is '{applicant.stage_id.name}', expected 'First Interview'"
        )

    skills = applicant.applicant_skill_ids.filtered(
        lambda skill: skill.skill_id.name == "Python"
    )
    if len(skills) != 1:
        failures.append(f"Expected 1 Python skill entry, found {len(skills)}")
    else:
        skill = skills[0]
        if skill.skill_type_id.name != "IT Skills":
            failures.append(
                f"Skill type is '{skill.skill_type_id.name}', expected 'IT Skills'"
            )
        if skill.skill_level_id.name != "Advanced":
            failures.append(
                f"Skill level is '{skill.skill_level_id.name}', expected 'Advanced'"
            )

    if len(applicant.applicant_skill_ids) != 1:
        failures.append(
            f"Expected exactly 1 applicant skill entry, found {len(applicant.applicant_skill_ids)}"
        )

    return failures
