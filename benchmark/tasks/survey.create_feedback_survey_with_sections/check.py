"""Postcondition checks for survey.create_feedback_survey_with_sections."""


def check(env):
    failures = []

    if "survey.survey" not in env.registry:
        return ["survey module is not installed"]

    survey = env["survey.survey"].with_context(active_test=False).search([
        ("title", "=", "Q1 Workshop Feedback"),
    ], limit=1)
    if not survey:
        return ["Survey 'Q1 Workshop Feedback' not found"]

    # Survey must remain active (published / not archived).
    if not survey.active:
        failures.append("Survey is archived; expected to remain active")

    # Survey type must NOT be 'assessment' (per spec).
    if survey.survey_type == "assessment":
        failures.append(
            f"Survey type is '{survey.survey_type}', expected anything other than 'assessment'"
        )

    # Pagination: one page per section.
    if survey.questions_layout != "page_per_section":
        failures.append(
            f"Pagination is '{survey.questions_layout}', expected 'page_per_section'"
        )

    # Access mode: public (anyone with the link).
    if survey.access_mode != "public":
        failures.append(
            f"Access mode is '{survey.access_mode}', expected 'public'"
        )

    # Time limit enabled and equal to 10 minutes.
    if not survey.is_time_limited:
        failures.append("Time limit is not enabled")
    # time_limit is a Float (minutes) in Odoo 19.
    if abs((survey.time_limit or 0.0) - 10.0) > 1e-3:
        failures.append(
            f"Time limit is {survey.time_limit}, expected 10 minutes"
        )

    # Must not be a certification.
    if survey.certification:
        failures.append("Survey should not be a certification")

    # --- Sections (pages) and questions ---
    pages = survey.question_and_page_ids.filtered(lambda q: q.is_page)
    questions = survey.question_and_page_ids.filtered(lambda q: not q.is_page)

    if len(pages) != 2:
        failures.append(f"Expected 2 sections, found {len(pages)}")
    if len(questions) != 4:
        failures.append(f"Expected 4 questions, found {len(questions)}")

    # Section titles
    page_titles = set(pages.mapped("title"))
    for needed in ("Content", "Logistics"):
        if needed not in page_titles:
            failures.append(f"Missing section titled '{needed}' (found sections: {sorted(page_titles)})")

    # Question titles
    q_titles = set(questions.mapped("title"))
    expected_q_titles = {
        "How clear was the material?",
        "Rate the pace",
        "Was the venue comfortable?",
        "Comments",
    }
    missing = expected_q_titles - q_titles
    if missing:
        failures.append(f"Missing question(s): {sorted(missing)} (found: {sorted(q_titles)})")

    # Type checks per question (lenient where allowed by prompt).
    by_title = {q.title: q for q in questions}

    q1 = by_title.get("How clear was the material?")
    if q1 and q1.question_type != "simple_choice":
        failures.append(
            f"'How clear was the material?' is type '{q1.question_type}', expected 'simple_choice'"
        )
    if q1:
        ans = sorted(q1.suggested_answer_ids.mapped("value"))
        if ans != sorted(["Very clear", "Clear", "Unclear"]):
            failures.append(
                f"Answers for 'How clear was the material?' are {ans}, expected ['Clear', 'Unclear', 'Very clear']"
            )

    q2 = by_title.get("Rate the pace")
    if q2 and q2.question_type not in ("scale", "numerical_box"):
        failures.append(
            f"'Rate the pace' is type '{q2.question_type}', expected 'scale' or 'numerical_box'"
        )

    q3 = by_title.get("Was the venue comfortable?")
    if q3 and q3.question_type != "simple_choice":
        failures.append(
            f"'Was the venue comfortable?' is type '{q3.question_type}', expected 'simple_choice'"
        )
    if q3:
        ans = sorted(q3.suggested_answer_ids.mapped("value"))
        if ans != sorted(["Yes", "No"]):
            failures.append(
                f"Answers for 'Was the venue comfortable?' are {ans}, expected ['No', 'Yes']"
            )

    q4 = by_title.get("Comments")
    if q4 and q4.question_type != "text_box":
        failures.append(
            f"'Comments' is type '{q4.question_type}', expected 'text_box'"
        )

    return failures
