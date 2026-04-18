"""Seed for event.add_event_questions_to_registration.

Creates a deterministic event named 'Bench Tech Conference 2026' with
no extra registration questions linked. The agent must add the two new
questions specified in the prompt via the Questions tab.
"""

EVENT_NAME = "Bench Tech Conference 2026"

# Titles the agent will create — clean these up so reruns are idempotent.
QUESTION_TITLES_TO_CLEANUP = [
    "What is your job title?",
    "How many years of experience?",
]


def setup(env):
    # Cleanup previous run: remove the event itself (which removes the M2M
    # links), then remove any agent-created event.question records that
    # might still be hanging around (they are reusable so they are not
    # auto-deleted with the event).
    events = env["event.event"].with_context(active_test=False).search([
        ("name", "=", EVENT_NAME),
    ])
    if events:
        # Detach any registration answers first to avoid the unlink guard.
        registrations = events.registration_ids
        if registrations:
            registrations.registration_answer_ids.unlink()
            registrations.unlink()
        events.unlink()

    # Remove orphaned event.question records left over from prior runs so
    # the diff engine starts from a clean slate.
    leftover = env["event.question"].with_context(active_test=False).search([
        ("title", "in", QUESTION_TITLES_TO_CLEANUP),
        ("event_ids", "=", False),
        ("event_type_ids", "=", False),
    ])
    if leftover:
        leftover.answer_ids.unlink()
        leftover.unlink()

    env.flush_all()

    # Create the event with no extra questions linked. Use no event_type_id
    # so the default template question set is empty for this seed.
    env["event.event"].create({
        "name": EVENT_NAME,
        "date_begin": "2026-09-15 09:00:00",
        "date_end": "2026-09-17 17:00:00",
    })
