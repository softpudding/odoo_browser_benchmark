"""Postcondition checks for hr_recruitment.create_applicant_add_skills_refuse.

Validates:
1. Applicant "Cameron Blake" exists with correct email, phone, and job.
2. Applicant has exactly one skill: Python / Languages / Advanced.
3. Applicant is refused (active=False, refuse_reason_id set correctly).
4. Distractor "Cameron Brooks" is unchanged (active, no refuse reason).
"""

JOB_NAME = "Senior Data Engineer"
TARGET = "Cameron Blake"
DISTRACTOR = "Cameron Brooks"
EXPECTED_EMAIL = "cameron.blake@techmail.example.com"
EXPECTED_PHONE = "+1 555 0147"
EXPECTED_REASON = "Does not fit the job requirements"


def check(env):
    failures = []
    Applicant = env["hr.applicant"].with_context(active_test=False)

    # --- Target applicant ---
    target = Applicant.search([
        ("partner_name", "=", TARGET),
    ], limit=1)
    if not target:
        return [f"Target applicant '{TARGET}' not found"]

    # Check job
    if target.job_id.name != JOB_NAME:
        failures.append(
            f"Job is '{target.job_id.name}', expected '{JOB_NAME}'"
        )

    # Check email
    if target.email_from != EXPECTED_EMAIL:
        failures.append(
            f"Email is '{target.email_from}', expected '{EXPECTED_EMAIL}'"
        )

    # Check phone
    if target.partner_phone != EXPECTED_PHONE:
        failures.append(
            f"Phone is '{target.partner_phone}', expected '{EXPECTED_PHONE}'"
        )

    # Check skill
    skills = target.applicant_skill_ids
    if len(skills) != 1:
        failures.append(f"Expected exactly 1 skill, found {len(skills)}")
    else:
        skill = skills[0]
        if skill.skill_id.name != "Python":
            failures.append(
                f"Skill is '{skill.skill_id.name}', expected 'Python'"
            )
        if skill.skill_type_id.name != "Languages":
            failures.append(
                f"Skill type is '{skill.skill_type_id.name}', expected 'Languages'"
            )
        if skill.skill_level_id.name != "Advanced":
            failures.append(
                f"Skill level is '{skill.skill_level_id.name}', expected 'Advanced'"
            )

    # Check refused state
    if target.active:
        failures.append(
            f"Target applicant '{TARGET}' is still active (expected refused / archived)"
        )
    if not target.refuse_reason_id:
        failures.append(
            f"Target applicant '{TARGET}' has no refuse_reason_id set"
        )
    elif target.refuse_reason_id.name != EXPECTED_REASON:
        failures.append(
            f"Refuse reason is '{target.refuse_reason_id.name}', "
            f"expected '{EXPECTED_REASON}'"
        )

    # --- Distractor applicant ---
    distractor = Applicant.search([
        ("partner_name", "=", DISTRACTOR),
        ("job_id.name", "=", JOB_NAME),
    ], limit=1)
    if not distractor:
        failures.append(f"Distractor applicant '{DISTRACTOR}' is missing")
    else:
        if not distractor.active:
            failures.append(
                f"Distractor applicant '{DISTRACTOR}' was archived (expected active)"
            )
        if distractor.refuse_reason_id:
            failures.append(
                f"Distractor applicant '{DISTRACTOR}' has refuse_reason_id "
                f"'{distractor.refuse_reason_id.name}' (expected none)"
            )

    return failures
