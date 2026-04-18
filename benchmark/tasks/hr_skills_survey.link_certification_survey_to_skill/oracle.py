"""Oracle for hr_skills_survey.link_certification_survey_to_skill.

BLOCKED TASK — the `survey_id` / Certification many2one on `hr.skill`
does not exist in Odoo 19 Community. The oracle exits with a clear
error so the harness records the blocker instead of producing spurious
results.

To flesh out once the enterprise skill-certification link is available:
  1. Navigate to /odoo/surveys → New → fill title 'Bench Python Cert',
     survey_type='certification', scoring_type='scoring_with_answers',
     scoring_success_min=70, add two simple_choice questions with scored
     answers. Save.
  2. Navigate to /odoo/action-hr_skills.hr_skill_type_action → open
     'Programming Languages' → open 'Python' → set Certification =
     'Bench Python Cert'. Save.
  3. (Optional) Open the survey's Test link, answer correctly, submit,
     and verify the admin employee form surfaces the cert.
"""

from benchmark.oracle_helpers import run_oracle


def oracle(page):
    raise RuntimeError(
        "BLOCKED: hr.skill has no survey_id field in Odoo 19 Community "
        "(Enterprise-only). Oracle body intentionally short-circuits. "
        "See STATUS.md row 387."
    )


run_oracle(oracle)
