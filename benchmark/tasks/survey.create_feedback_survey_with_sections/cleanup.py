"""Cleanup for survey.create_feedback_survey_with_sections."""


def cleanup(env):
    if "survey.survey" not in env.registry:
        return
    survey = env["survey.survey"].with_context(active_test=False).search([
        ("title", "=", "Q1 Workshop Feedback"),
    ])
    if survey:
        survey.question_and_page_ids.unlink()
        survey.unlink()
