"""Postcondition checks for website_slides.add_quiz_lesson_to_existing_course."""


EXPECTED_QUESTIONS = [
    {
        "question": "What is the primary color of the Bench logo?",
        "answers": ["Blue", "Red", "Green"],
        "correct": "Blue",
    },
    {
        "question": "How often do we stand up?",
        "answers": ["Daily", "Weekly", "Never"],
        "correct": "Daily",
    },
    {
        "question": "Which team owns shared infra?",
        "answers": ["Platform", "Product", "Growth"],
        "correct": "Platform",
    },
]


def check(env):
    failures = []

    course = env["slide.channel"].with_context(active_test=False).search([
        ("name", "=", "Bench Onboarding Course"),
    ], limit=1)
    if not course:
        return ["Course 'Bench Onboarding Course' not found"]
    if not course.website_published:
        failures.append("Course is not published")

    # Distractor: Welcome Video should still exist on the course unchanged.
    welcome = env["slide.slide"].with_context(active_test=False).search([
        ("name", "=", "Welcome Video"),
        ("channel_id", "=", course.id),
    ])
    if len(welcome) != 1:
        failures.append(
            f"Expected exactly 1 'Welcome Video' slide on course, found {len(welcome)}"
        )
    else:
        if welcome.slide_category != "video":
            failures.append(
                f"Welcome Video slide_category is {welcome.slide_category!r}, expected 'video'"
            )
        if not welcome.website_published:
            failures.append("Welcome Video lesson is no longer published")

    quiz = env["slide.slide"].with_context(active_test=False).search([
        ("name", "=", "Chapter 1 Quiz"),
        ("channel_id", "=", course.id),
    ])
    if len(quiz) != 1:
        failures.append(
            f"Expected exactly 1 'Chapter 1 Quiz' slide on course, found {len(quiz)}"
        )
        return failures

    if quiz.slide_category != "quiz":
        failures.append(
            f"Chapter 1 Quiz slide_category is {quiz.slide_category!r}, expected 'quiz'"
        )
    if not quiz.website_published:
        failures.append("Chapter 1 Quiz lesson is not published")

    questions = quiz.question_ids
    if len(questions) != 3:
        failures.append(
            f"Expected exactly 3 questions on the quiz, found {len(questions)}"
        )

    for spec in EXPECTED_QUESTIONS:
        matching = questions.filtered(lambda q, t=spec["question"]: q.question == t)
        if len(matching) != 1:
            failures.append(
                f"Expected exactly 1 question titled {spec['question']!r}, "
                f"found {len(matching)}"
            )
            continue
        question = matching
        answers = question.answer_ids
        if len(answers) != 3:
            failures.append(
                f"Question {spec['question']!r} has {len(answers)} answers, "
                f"expected 3"
            )
            continue

        actual_values = sorted(answers.mapped("text_value"))
        expected_values = sorted(spec["answers"])
        if actual_values != expected_values:
            failures.append(
                f"Question {spec['question']!r} answers are {actual_values}, "
                f"expected {expected_values}"
            )
            continue

        correct = answers.filtered("is_correct")
        if len(correct) != 1:
            failures.append(
                f"Question {spec['question']!r} must have exactly 1 correct "
                f"answer, found {len(correct)}"
            )
            continue
        if correct.text_value != spec["correct"]:
            failures.append(
                f"Question {spec['question']!r} correct answer is "
                f"{correct.text_value!r}, expected {spec['correct']!r}"
            )

    return failures
