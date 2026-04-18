"""Postcondition checks for website_event.publish_event_register_via_portal."""

EVENT_NAME = "Bench Public Day"
ATTENDEE_NAME = "Priya Patel"
ATTENDEE_EMAIL = "priya.patel@example.com"
ATTENDEE_PHONE = "+1 555 0142"


def check(env):
    failures = []

    events = env["event.event"].with_context(active_test=False).search([
        ("name", "=", EVENT_NAME),
    ])
    if not events:
        return [f"No event.event named '{EVENT_NAME}' — seed failed"]
    if len(events) > 1:
        failures.append(
            f"Expected exactly 1 event named '{EVENT_NAME}', found {len(events)}"
        )
    event = events[0]

    if not event.is_published:
        failures.append(
            f"Event '{EVENT_NAME}' is_published is False — expected True"
        )

    regs = env["event.registration"].with_context(active_test=False).search([
        ("event_id", "=", event.id),
        ("name", "=", ATTENDEE_NAME),
    ])
    if not regs:
        failures.append(
            f"No event.registration for '{ATTENDEE_NAME}' on '{EVENT_NAME}'"
        )
        return failures
    if len(regs) > 1:
        failures.append(
            f"Expected exactly 1 registration for '{ATTENDEE_NAME}' on "
            f"'{EVENT_NAME}', found {len(regs)}"
        )
    reg = regs[0]

    if (reg.email or "").strip().lower() != ATTENDEE_EMAIL.lower():
        failures.append(
            f"Registration email is {reg.email!r}, expected {ATTENDEE_EMAIL!r}"
        )

    # State should be 'open' (Registered) — that's the default for a
    # freshly-submitted public registration.
    if reg.state != "open":
        failures.append(
            f"Registration state is {reg.state!r}, expected 'open'"
        )

    # Phone is nice-to-have; accept any value containing the digits to be
    # tolerant of formatting (agents sometimes drop the leading +1).
    if reg.phone:
        digits_expected = "".join(c for c in ATTENDEE_PHONE if c.isdigit())
        digits_actual = "".join(c for c in (reg.phone or "") if c.isdigit())
        if digits_expected not in digits_actual:
            failures.append(
                f"Registration phone is {reg.phone!r}, expected to contain "
                f"the digits of {ATTENDEE_PHONE!r}"
            )

    # Sanity: no stray registrations created on other events with the
    # same attendee name.
    extras = env["event.registration"].with_context(active_test=False).search([
        ("name", "=", ATTENDEE_NAME),
        ("event_id", "!=", event.id),
    ])
    if extras:
        failures.append(
            f"Found {len(extras)} extra registration(s) for "
            f"'{ATTENDEE_NAME}' on other events"
        )

    # Sanity: no stray Bench Public Day events were created beyond the seed.
    if len(events) != 1:
        failures.append(
            f"Expected exactly 1 event named '{EVENT_NAME}', found {len(events)}"
        )

    return failures
