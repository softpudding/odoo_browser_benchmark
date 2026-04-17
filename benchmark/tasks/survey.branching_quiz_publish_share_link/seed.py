"""Seed for survey.branching_quiz_publish_share_link."""


def setup(env):
    survey = env["survey.survey"].with_context(active_test=False).search([
        ("title", "=", "Dock Safety Branching Quiz"),
    ])
    if survey:
        survey.question_and_page_ids.unlink()
        survey.unlink()
