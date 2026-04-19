"""Postcondition checks for website_event.add_sponsor_to_event_publish."""


EVENT_NAME = "Bench Conf 2026"
PARTNER_NAME = "Bench Sponsor Inc"
SPONSOR_LEVEL = "Silver"


def check(env):
    failures = []

    events = env["event.event"].search([("name", "=", EVENT_NAME)])
    if len(events) != 1:
        return [f"Expected exactly 1 event named '{EVENT_NAME}', found {len(events)}"]
    event = events[0]

    # ----- Publish flag -----
    if not event.is_published:
        failures.append(
            f"Event '{EVENT_NAME}' is_published is False, expected True"
        )

    # ----- Sponsor row -----
    sponsors = env["event.sponsor"].with_context(active_test=False).search([
        ("event_id", "=", event.id),
    ])
    if len(sponsors) != 1:
        return failures + [
            f"Expected exactly 1 event.sponsor on '{EVENT_NAME}', found {len(sponsors)}"
        ]
    sponsor = sponsors[0]

    if (sponsor.partner_id.name or "").strip() != PARTNER_NAME:
        failures.append(
            f"Sponsor partner is {sponsor.partner_id.name!r}, expected {PARTNER_NAME!r}"
        )

    if (sponsor.sponsor_type_id.name or "").strip() != SPONSOR_LEVEL:
        failures.append(
            f"Sponsor level is {sponsor.sponsor_type_id.name!r}, expected {SPONSOR_LEVEL!r}"
        )

    # Guardrail: no extra sponsors on the partner across the DB should be
    # created (the agent should not have duplicated the sponsor). We only
    # care about sponsors on our event here, already asserted via count==1.

    # Guardrail: event name unchanged.
    if event.name != EVENT_NAME:
        failures.append(f"Event name changed to {event.name!r}")

    # Guardrail: no registrations created as a side effect.
    regs = env["event.registration"].with_context(active_test=False).search([
        ("event_id", "=", event.id),
    ])
    if regs:
        failures.append(
            f"Unexpected event.registration records on '{EVENT_NAME}': "
            f"{regs.mapped('name')}"
        )

    return failures
