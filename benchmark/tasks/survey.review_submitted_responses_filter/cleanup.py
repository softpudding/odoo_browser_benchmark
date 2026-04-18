"""Cleanup for survey.review_submitted_responses_filter."""

SURVEY_TITLE = "Customer Pulse March"


def cleanup(env):
    surveys = env["survey.survey"].with_context(active_test=False).search([
        ("title", "=", SURVEY_TITLE),
    ])
    if surveys:
        env["survey.user_input"].with_context(active_test=False).search([
            ("survey_id", "in", surveys.ids),
        ]).unlink()
        surveys.question_and_page_ids.unlink()
        surveys.unlink()
