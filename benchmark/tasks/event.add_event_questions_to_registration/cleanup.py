"""Cleanup for event.add_event_questions_to_registration."""

EVENT_NAME = "Bench Tech Conference 2026"

# Mirrors the question titles the agent (or oracle) creates.
QUESTION_TITLES = [
    "What is your job title?",
    "How many years of experience?",
]


def cleanup(env):
    events = env["event.event"].with_context(active_test=False).search([
        ("name", "=", EVENT_NAME),
    ])
    if events:
        registrations = events.registration_ids
        if registrations:
            registrations.registration_answer_ids.unlink()
            registrations.unlink()
        events.unlink()

    leftover = env["event.question"].with_context(active_test=False).search([
        ("title", "in", QUESTION_TITLES),
        ("event_ids", "=", False),
        ("event_type_ids", "=", False),
    ])
    if leftover:
        leftover.answer_ids.unlink()
        leftover.unlink()
