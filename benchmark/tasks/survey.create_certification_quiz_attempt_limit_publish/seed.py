"""Seed for survey.create_certification_quiz_attempt_limit_publish."""


SURVEY_TITLE = "Forklift Safety Certification"


def setup(env):
    env["survey.survey"].with_context(active_test=False).search([
        ("title", "=", SURVEY_TITLE),
    ]).unlink()
