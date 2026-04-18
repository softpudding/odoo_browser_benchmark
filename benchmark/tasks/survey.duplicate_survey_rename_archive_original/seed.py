"""Seed for survey.duplicate_survey_rename_archive_original."""

ORIGINAL_TITLE = "Quarterly Pulse Q1 Template"
COPY_TITLE = "Quarterly Pulse Q2 2026"


def setup(env):
    surveys = env["survey.survey"].with_context(active_test=False).search([
        ("title", "in", [ORIGINAL_TITLE, COPY_TITLE, f"{ORIGINAL_TITLE} (copy)"]),
    ])
    if surveys:
        env["survey.user_input"].with_context(active_test=False).search([
            ("survey_id", "in", surveys.ids),
        ]).unlink()
        surveys.question_and_page_ids.unlink()
        surveys.unlink()

    survey = env["survey.survey"].create({
        "title": ORIGINAL_TITLE,
        "survey_type": "survey",
        "questions_layout": "one_page",
        "access_mode": "public",
        "scoring_type": "no_scoring",
        "active": True,
    })

    q1 = env["survey.question"].create({
        "survey_id": survey.id,
        "title": "How would you rate this quarter overall?",
        "sequence": 10,
        "question_type": "simple_choice",
        "constr_mandatory": True,
    })
    for value in ("Excellent", "Good", "Fair", "Poor"):
        env["survey.question.answer"].create({
            "question_id": q1.id,
            "value": value,
        })
    env["survey.question"].create({
        "survey_id": survey.id,
        "title": "What should we improve?",
        "sequence": 20,
        "question_type": "text_box",
    })
