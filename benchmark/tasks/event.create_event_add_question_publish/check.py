"""Postcondition checks for event.create_event_add_question_publish."""

EVENT_NAME = "Bench 2026 Conference"
Q1_TITLE = "Company"
Q2_TITLE = "Experience Level"
Q2_ANSWERS = ["Beginner", "Intermediate", "Expert"]


def check(env):
    failures = []

    events = env["event.event"].with_context(active_test=False).search([
        ("name", "=", EVENT_NAME),
    ])
    if not events:
        return [f"No event.event named '{EVENT_NAME}' — agent did not create it"]
    if len(events) > 1:
        failures.append(
            f"Expected exactly 1 event named '{EVENT_NAME}', found {len(events)}"
        )
    event = events[0]

    # ----- Publish flags -----
    if not event.is_published:
        failures.append(
            f"Event '{EVENT_NAME}' is_published is False — expected True"
        )
    if not event.website_published:
        failures.append(
            f"Event '{EVENT_NAME}' website_published is False — expected True"
        )

    # ----- Questions on this event -----
    # The agent must add TWO new questions on top of any default questions
    # auto-attached by _compute_question_ids (Name, Email, Phone are default).
    q1s = event.question_ids.filtered(lambda q: q.title == Q1_TITLE)
    if len(q1s) != 1:
        failures.append(
            f"Expected exactly 1 question titled '{Q1_TITLE}' on event, found {len(q1s)}"
        )
    else:
        q1 = q1s[0]
        if q1.question_type != "text_box":
            failures.append(
                f"Question '{Q1_TITLE}' question_type is {q1.question_type!r}, "
                f"expected 'text_box'"
            )
        if not q1.is_mandatory_answer:
            failures.append(
                f"Question '{Q1_TITLE}' is_mandatory_answer is False, expected True"
            )
        if q1.once_per_order:
            failures.append(
                f"Question '{Q1_TITLE}' once_per_order is True, "
                f"expected False (ask per attendee)"
            )

    q2s = event.question_ids.filtered(lambda q: q.title == Q2_TITLE)
    if len(q2s) != 1:
        failures.append(
            f"Expected exactly 1 question titled '{Q2_TITLE}' on event, found {len(q2s)}"
        )
    else:
        q2 = q2s[0]
        if q2.question_type != "simple_choice":
            failures.append(
                f"Question '{Q2_TITLE}' question_type is {q2.question_type!r}, "
                f"expected 'simple_choice'"
            )
        if not q2.is_mandatory_answer:
            failures.append(
                f"Question '{Q2_TITLE}' is_mandatory_answer is False, expected True"
            )
        if q2.once_per_order:
            failures.append(
                f"Question '{Q2_TITLE}' once_per_order is True, expected False"
            )
        # Nested answer rows.
        actual_answers = [a.name for a in q2.answer_ids.sorted("sequence")]
        if set(actual_answers) != set(Q2_ANSWERS):
            failures.append(
                f"Question '{Q2_TITLE}' answers are {actual_answers!r}, "
                f"expected {Q2_ANSWERS!r}"
            )
        elif len(q2.answer_ids) != len(Q2_ANSWERS):
            failures.append(
                f"Question '{Q2_TITLE}' has {len(q2.answer_ids)} answers, "
                f"expected exactly {len(Q2_ANSWERS)}"
            )

    # ----- Guardrail: no extra Bench 2026 Conference events -----
    # Already checked via len(events) above.

    # ----- Guardrail: no registrations were created -----
    regs = env["event.registration"].with_context(active_test=False).search([
        ("event_id", "=", event.id),
    ])
    if regs:
        failures.append(
            f"Unexpected event.registration records on '{EVENT_NAME}': "
            f"{regs.mapped('name')}"
        )

    return failures
