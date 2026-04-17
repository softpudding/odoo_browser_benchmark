"""Postcondition checks for survey.branching_quiz_publish_share_link."""


def check(env):
    failures = []

    survey = env["survey.survey"].with_context(active_test=False).search([
        ("title", "=", "Dock Safety Branching Quiz"),
    ], limit=1)
    if not survey:
        return ["Survey 'Dock Safety Branching Quiz' not found"]

    if survey.questions_layout != "one_page":
        failures.append(
            f"Survey pagination is '{survey.questions_layout}', expected 'one_page'"
        )
    if survey.scoring_type == "no_scoring":
        failures.append("Survey scoring is disabled")
    if survey.access_mode != "public":
        failures.append(f"Survey access mode is '{survey.access_mode}', expected 'public'")
    if not survey.access_token:
        failures.append("Survey is missing a share access token")
    if survey.certification:
        failures.append("Survey should not be a certification")

    q1 = survey.question_ids.filtered(
        lambda q: q.title == "Which dock zone requires extra clearance tonight?"
    )
    q2 = survey.question_ids.filtered(
        lambda q: q.title == "Why is Zone B restricted tonight?"
    )
    if len(q1) != 1:
        failures.append(f"Expected 1 first question, found {len(q1)}")
        return failures
    if len(q2) != 1:
        failures.append(f"Expected 1 conditional question, found {len(q2)}")
        return failures

    q1 = q1[0]
    q2 = q2[0]
    if q1.question_type != "simple_choice":
        failures.append(f"First question type is '{q1.question_type}', expected 'simple_choice'")
    if q2.question_type != "text_box":
        failures.append(f"Conditional question type is '{q2.question_type}', expected 'text_box'")

    answers = q1.suggested_answer_ids.sorted("value")
    answer_values = answers.mapped("value")
    if answer_values != ["Zone A", "Zone B"]:
        failures.append(f"First question answers are {answer_values}, expected ['Zone A', 'Zone B']")
    else:
        zone_b = answers.filtered(lambda a: a.value == "Zone B")
        if not zone_b or not zone_b[0].is_correct:
            failures.append("Zone B is not marked as the correct answer")
        if q2.triggering_answer_ids != zone_b:
            failures.append("Conditional question is not triggered only by the Zone B answer")

    return failures
