"""Cleanup for survey.create_certification_quiz_attempt_limit_publish."""


def cleanup(env):
    env["survey.survey"].with_context(active_test=False).search([
        ("title", "=", "Forklift Safety Certification"),
    ]).unlink()
