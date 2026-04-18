"""Cleanup for survey.duplicate_survey_rename_archive_original."""

ORIGINAL_TITLE = "Quarterly Pulse Q1 Template"
COPY_TITLE = "Quarterly Pulse Q2 2026"


def cleanup(env):
    surveys = env["survey.survey"].with_context(active_test=False).search([
        ("title", "in", [ORIGINAL_TITLE, COPY_TITLE, f"{ORIGINAL_TITLE} (copy)"]),
    ])
    if surveys:
        env["survey.user_input"].with_context(active_test=False).search([
            ("survey_id", "in", surveys.ids),
        ]).unlink()
        surveys.question_and_page_ids.unlink()
        surveys.unlink()
