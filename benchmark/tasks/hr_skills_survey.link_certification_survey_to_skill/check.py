"""Postcondition checks for hr_skills_survey.link_certification_survey_to_skill.

BLOCKED TASK — hr.skill has no `survey_id` field in Odoo 19 Community, so
the task cannot run end-to-end. The check below returns a clear failure
string so the eval pipeline flags it rather than appearing as a spurious
PASS.
"""


def check(env):
    if "survey_id" not in env["hr.skill"]._fields:
        return [
            "BLOCKED: `hr.skill.survey_id` is not available in this Odoo "
            "Community checkout (Enterprise-only). Task cannot be validated "
            "end-to-end. See STATUS.md row 387 for re-enabling notes."
        ]

    # Concrete validation to add once the field is available:
    #   - exactly one `survey.survey` titled 'Bench Python Cert' with
    #     survey_type='certification' and scoring_success_min==70.0.
    #   - `hr.skill` with name='Python' has survey_id == the above survey.
    #   - (optional) admin employee has exactly one hr.employee.skill row
    #     for Python with skill_type_id.is_certification == True and a
    #     non-empty valid_to.
    return [
        "BLOCKED: hr.skill.survey_id became available but check body not "
        "yet implemented. See STATUS.md row 387 for context."
    ]
