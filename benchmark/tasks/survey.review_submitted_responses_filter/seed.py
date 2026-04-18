"""Seed for survey.review_submitted_responses_filter.

Creates a survey "Customer Pulse March" with two questions and four
completed user_input records. Two are dated March 5 2026 and two are
dated March 20 2026. The third record (the target) uses the email
``reviewer-target@example.com`` so the agent must locate it among
distractors before posting a chatter message.
"""

SURVEY_TITLE = "Customer Pulse March"
TARGET_EMAIL = "reviewer-target@example.com"
DISTRACTOR_EMAILS = [
    "alice.kim@example.com",
    "bob.lee@example.com",
    "diana.wong@example.com",
]


def _delete_existing(env):
    surveys = env["survey.survey"].with_context(active_test=False).search([
        ("title", "=", SURVEY_TITLE),
    ])
    if surveys:
        env["survey.user_input"].with_context(active_test=False).search([
            ("survey_id", "in", surveys.ids),
        ]).unlink()
        surveys.question_and_page_ids.unlink()
        surveys.unlink()


def setup(env):
    _delete_existing(env)

    survey = env["survey.survey"].create({
        "title": SURVEY_TITLE,
        "survey_type": "survey",
        "questions_layout": "one_page",
        "access_mode": "token",
        "scoring_type": "no_scoring",
    })

    q1 = env["survey.question"].create({
        "survey_id": survey.id,
        "title": "How would you rate our service this month?",
        "sequence": 10,
        "question_type": "simple_choice",
        "constr_mandatory": True,
    })
    answers = []
    for value in ("Excellent", "Good", "Fair", "Poor"):
        answers.append(env["survey.question.answer"].create({
            "question_id": q1.id,
            "value": value,
        }))
    env["survey.question"].create({
        "survey_id": survey.id,
        "title": "Anything you'd like us to improve?",
        "sequence": 20,
        "question_type": "text_box",
    })

    # Order: distractor (Mar 5), distractor (Mar 5), TARGET (Mar 20),
    # distractor (Mar 20). The target is the only one with the special email.
    plan = [
        (DISTRACTOR_EMAILS[0], "2026-03-05 09:15:00", answers[1]),  # Good
        (DISTRACTOR_EMAILS[1], "2026-03-05 14:42:00", answers[0]),  # Excellent
        (TARGET_EMAIL,         "2026-03-20 10:30:00", answers[2]),  # Fair
        (DISTRACTOR_EMAILS[2], "2026-03-20 16:05:00", answers[1]),  # Good
    ]

    for email, ts, chosen in plan:
        ui = env["survey.user_input"].create({
            "survey_id": survey.id,
            "email": email,
            "state": "done",
            "start_datetime": ts,
            "end_datetime": ts,
        })
        env["survey.user_input.line"].create({
            "user_input_id": ui.id,
            "question_id": q1.id,
            "survey_id": survey.id,
            "answer_type": "suggestion",
            "suggested_answer_id": chosen.id,
        })
        # Force create_date so the list view ordering and any date filter
        # behave as described in the prompt.
        env.cr.execute(
            "UPDATE survey_user_input SET create_date = %s, write_date = %s WHERE id = %s",
            (ts, ts, ui.id),
        )

    env.cr.commit()
