"""Postcondition checks for event.add_event_questions_to_registration."""


EVENT_NAME = "Bench Tech Conference 2026"
TEXT_QUESTION = "What is your job title?"
SELECTION_QUESTION = "How many years of experience?"
SELECTION_ANSWERS = ["0-2", "3-5", "5+"]


def check(env):
    failures = []

    event = env["event.event"].search([("name", "=", EVENT_NAME)], limit=1)
    if not event:
        return [f"Event '{EVENT_NAME}' not found"]

    questions = event.question_ids
    by_title = {q.title: q for q in questions}

    if TEXT_QUESTION not in by_title:
        failures.append(
            f"Missing question titled '{TEXT_QUESTION}' on event "
            f"(found: {sorted(by_title)})"
        )
    else:
        q = by_title[TEXT_QUESTION]
        if q.question_type != "text_box":
            failures.append(
                f"'{TEXT_QUESTION}' is type '{q.question_type}', "
                f"expected 'text_box' (Text Input)"
            )

    if SELECTION_QUESTION not in by_title:
        failures.append(
            f"Missing question titled '{SELECTION_QUESTION}' on event "
            f"(found: {sorted(by_title)})"
        )
    else:
        q = by_title[SELECTION_QUESTION]
        if q.question_type != "simple_choice":
            failures.append(
                f"'{SELECTION_QUESTION}' is type '{q.question_type}', "
                f"expected 'simple_choice' (Selection)"
            )
        else:
            answers = sorted(q.answer_ids.mapped("name"))
            if answers != sorted(SELECTION_ANSWERS):
                failures.append(
                    f"Answers for '{SELECTION_QUESTION}' are {answers}, "
                    f"expected {sorted(SELECTION_ANSWERS)}"
                )

    return failures
