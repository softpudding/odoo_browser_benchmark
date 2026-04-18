"""Seed for survey.create_survey_one_page_publish_share.

Ensures the survey module is installed and removes any prior survey with the
target title. The agent must create the survey from scratch.
"""

SURVEY_TITLE = "Bench Customer Feedback"


def _ensure_survey_module(env):
    survey_mod = env["ir.module.module"].search([("name", "=", "survey")], limit=1)
    if survey_mod and survey_mod.state != "installed":
        survey_mod.button_immediate_install()


def setup(env):
    _ensure_survey_module(env)

    if "survey.survey" not in env.registry:
        return

    surveys = env["survey.survey"].with_context(active_test=False).search([
        ("title", "=", SURVEY_TITLE),
    ])
    if surveys:
        env["survey.user_input"].with_context(active_test=False).search([
            ("survey_id", "in", surveys.ids),
        ]).unlink()
        surveys.question_and_page_ids.unlink()
        surveys.unlink()
