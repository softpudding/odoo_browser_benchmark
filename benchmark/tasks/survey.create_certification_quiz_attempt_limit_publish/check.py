"""Postcondition checks for survey.create_certification_quiz_attempt_limit_publish."""


SURVEY_TITLE = "Forklift Safety Certification"
DESCRIPTION = "Pass this certification before operating lift equipment."

EXPECTED_QUESTIONS = [
    (
        "What is the maximum load for Bay 3 forklift?",
        ["800 kg", "1200 kg", "1600 kg"],
        "1200 kg",
    ),
    (
        "When reversing with a blocked view, what must the operator do?",
        ["Use a spotter", "Speed up to clear the aisle", "Lift the forks higher"],
        "Use a spotter",
    ),
    (
        "Where is the emergency cutoff for Charging Station B?",
        ["North wall", "Inside the battery cabinet", "By the loading door"],
        "North wall",
    ),
    (
        "After a hydraulic leak, what is the first action?",
        [
            "Shut down the forklift and isolate the area",
            "Finish the delivery before reporting it",
            "Wash the leak into the nearest drain",
        ],
        "Shut down the forklift and isolate the area",
    ),
]


def check(env):
    failures = []

    survey = env["survey.survey"].with_context(active_test=False).search([
        ("title", "=", SURVEY_TITLE),
    ], limit=1)
    if not survey:
        return [f"Survey {SURVEY_TITLE!r} not found"]

    if not survey.active:
        failures.append("Survey is archived; expected active")
    if DESCRIPTION not in (survey.description or ""):
        failures.append("Survey description does not contain the expected text")
    if survey.questions_layout != "page_per_section":
        failures.append(
            f"Pagination is {survey.questions_layout!r}, expected 'page_per_section'"
        )
    if survey.access_mode != "token":
        failures.append(f"Access mode is {survey.access_mode!r}, expected 'token'")
    if not survey.access_token:
        failures.append("Survey is missing an invite access token")
    if survey.scoring_type != "scoring_with_answers":
        failures.append(
            f"Scoring type is {survey.scoring_type!r}, expected 'scoring_with_answers'"
        )
    if not survey.certification:
        failures.append("Certification is not enabled")
    if abs((survey.scoring_success_min or 0.0) - 80.0) > 1e-3:
        failures.append(
            f"Passing score is {survey.scoring_success_min}, expected 80"
        )
    if not survey.is_attempts_limited:
        failures.append("Attempt limit is not enabled")
    if survey.attempts_limit != 2:
        failures.append(
            f"Attempts limit is {survey.attempts_limit}, expected 2"
        )

    pages = survey.question_and_page_ids.filtered(lambda q: q.is_page).sorted("sequence")
    if [p.title for p in pages] != ["Load Handling", "Emergency Response"]:
        failures.append(
            f"Section titles are {[p.title for p in pages]}, expected ['Load Handling', 'Emergency Response']"
        )

    questions = survey.question_and_page_ids.filtered(lambda q: not q.is_page).sorted("sequence")
    if len(questions) != 4:
        failures.append(f"Expected 4 questions, found {len(questions)}")
        return failures

    question_by_title = {q.title: q for q in questions}
    for title, expected_answers, correct_answer in EXPECTED_QUESTIONS:
        question = question_by_title.get(title)
        if not question:
            failures.append(f"Missing question {title!r}")
            continue
        if question.question_type != "simple_choice":
            failures.append(
                f"Question {title!r} has type {question.question_type!r}, expected 'simple_choice'"
            )
        answers = question.suggested_answer_ids.sorted("sequence")
        answer_values = answers.mapped("value")
        if answer_values != expected_answers:
            failures.append(
                f"Answers for {title!r} are {answer_values}, expected {expected_answers}"
            )
            continue
        correct = answers.filtered(lambda a: a.is_correct)
        if len(correct) != 1 or correct[0].value != correct_answer:
            failures.append(
                f"Correct answer for {title!r} is {[a.value for a in correct]}, expected {correct_answer!r}"
            )

    return failures
