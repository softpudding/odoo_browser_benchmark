"""Seed for survey.create_feedback_survey_with_sections.

Ensures the survey module is installed, then removes any prior survey
with the target title (active or archived).
"""


def _ensure_survey_module(env):
    survey_mod = env["ir.module.module"].search([("name", "=", "survey")], limit=1)
    if survey_mod and survey_mod.state != "installed":
        survey_mod.button_immediate_install()


def setup(env):
    _ensure_survey_module(env)

    if "survey.survey" not in env.registry:
        return

    survey = env["survey.survey"].with_context(active_test=False).search([
        ("title", "=", "Q1 Workshop Feedback"),
    ])
    if survey:
        survey.question_and_page_ids.unlink()
        survey.unlink()
