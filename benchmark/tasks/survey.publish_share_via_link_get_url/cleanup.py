"""Cleanup for survey.publish_share_via_link_get_url."""


SURVEY_TITLE = "Customer Pulse Q2"


def cleanup(env):
    if "survey.survey" not in env.registry:
        return
    survey = env["survey.survey"].with_context(active_test=False).search([
        ("title", "=", SURVEY_TITLE),
    ])
    if survey:
        survey.question_and_page_ids.unlink()
        survey.unlink()
