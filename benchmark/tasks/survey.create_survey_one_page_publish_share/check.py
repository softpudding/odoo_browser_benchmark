"""Postcondition checks for survey.create_survey_one_page_publish_share."""


SURVEY_TITLE = "Bench Customer Feedback"

Q1_TITLE = "How satisfied are you?"
Q2_TITLE = "What can we improve?"
Q3_TITLE = "Would you recommend us?"

Q1_ANSWERS = ["Very satisfied", "Satisfied", "Neutral", "Unsatisfied"]
Q3_ANSWERS = ["Yes", "No", "Maybe"]


def check(env):
    failures = []

    if "survey.survey" not in env.registry:
        return ["survey module is not installed"]

    Survey = env["survey.survey"].with_context(active_test=False)
    surveys = Survey.search([("title", "=", SURVEY_TITLE)])
    if len(surveys) != 1:
        return [
            f"Expected exactly 1 survey titled '{SURVEY_TITLE}', found {len(surveys)}"
        ]

    survey = surveys[0]

    if not survey.active:
        failures.append(f"Survey '{SURVEY_TITLE}' is archived; expected to stay active")

    if survey.access_mode != "public":
        failures.append(
            f"Access mode is '{survey.access_mode}', expected 'public' (Anyone with the link)"
        )

    if survey.certification:
        failures.append("Survey should not be a certification")

    # Questions only (exclude is_page section rows).
    questions = survey.question_and_page_ids.filtered(lambda q: not q.is_page)
    if len(questions) != 3:
        failures.append(f"Expected exactly 3 questions, found {len(questions)}")

    by_title = {q.title: q for q in questions}
    for needed in (Q1_TITLE, Q2_TITLE, Q3_TITLE):
        if needed not in by_title:
            failures.append(
                f"Missing question titled '{needed}' (found: {sorted(by_title)})"
            )

    q1 = by_title.get(Q1_TITLE)
    if q1:
        if q1.question_type != "simple_choice":
            failures.append(
                f"'{Q1_TITLE}' is type '{q1.question_type}', expected 'simple_choice'"
            )
        answers = sorted(q1.suggested_answer_ids.mapped("value"))
        if answers != sorted(Q1_ANSWERS):
            failures.append(
                f"Answers for '{Q1_TITLE}' are {answers}, expected {sorted(Q1_ANSWERS)}"
            )

    q2 = by_title.get(Q2_TITLE)
    if q2 and q2.question_type != "text_box":
        failures.append(
            f"'{Q2_TITLE}' is type '{q2.question_type}', expected 'text_box'"
        )

    q3 = by_title.get(Q3_TITLE)
    if q3:
        if q3.question_type != "simple_choice":
            failures.append(
                f"'{Q3_TITLE}' is type '{q3.question_type}', expected 'simple_choice'"
            )
        answers = sorted(q3.suggested_answer_ids.mapped("value"))
        if answers != sorted(Q3_ANSWERS):
            failures.append(
                f"Answers for '{Q3_TITLE}' are {answers}, expected {sorted(Q3_ANSWERS)}"
            )

    return failures
