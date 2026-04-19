"""Cleanup for event.create_event_add_question_publish."""

EVENT_NAME = "Bench 2026 Conference"
Q1_TITLE = "Company"
Q2_TITLE = "Experience Level"


def cleanup(env):
    # Drop the event first (will cascade to its m2m links on the questions).
    events = env["event.event"].with_context(active_test=False).search([
        ("name", "=", EVENT_NAME),
    ])
    events.mapped("registration_ids").sudo().unlink()
    events.mapped("event_ticket_ids").sudo().unlink()
    events.sudo().unlink()

    # Then remove the custom questions (they are reusable so would otherwise
    # linger across runs). Guard against answered questions.
    questions = env["event.question"].with_context(active_test=False).search([
        ("title", "in", [Q1_TITLE, Q2_TITLE]),
    ])
    for q in questions:
        try:
            q.sudo().unlink()
        except Exception:
            try:
                q.sudo().write({"active": False})
            except Exception:
                pass
