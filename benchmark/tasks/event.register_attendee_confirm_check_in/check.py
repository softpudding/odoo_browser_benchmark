"""Postcondition checks for event.register_attendee_confirm_check_in."""


EVENT_NAME = "Product Update Q2 — Partners Meetup"
ATTENDEE_NAME = "Sofia Reyes"
EXPECTED_EMAIL = "sofia.reyes@partner.example"
EXPECTED_PHONE = "+44 20 7946 0312"


def check(env):
    failures = []

    event = env["event.event"].search([("name", "=", EVENT_NAME)], limit=1)
    if not event:
        return [f"Event '{EVENT_NAME}' not found — seed failed"]

    regs = env["event.registration"].search([
        ("event_id", "=", event.id),
        ("name", "=", ATTENDEE_NAME),
    ])
    if not regs:
        return [
            f"No registration for '{ATTENDEE_NAME}' on event '{EVENT_NAME}'"
        ]
    if len(regs) > 1:
        failures.append(
            f"Found {len(regs)} registrations for {ATTENDEE_NAME}, expected 1"
        )
    reg = regs[0]

    if reg.state != "done":
        failures.append(
            f"Registration state is '{reg.state}', expected 'done' (attended)"
        )
    if reg.email != EXPECTED_EMAIL:
        failures.append(
            f"Email is '{reg.email}', expected '{EXPECTED_EMAIL}'"
        )
    if reg.phone and reg.phone.replace(" ", "") != EXPECTED_PHONE.replace(" ", ""):
        failures.append(
            f"Phone is '{reg.phone}', expected '{EXPECTED_PHONE}'"
        )

    # Sanity: no extra registrations were created with the same name.
    all_by_name = env["event.registration"].search([
        ("name", "=", ATTENDEE_NAME),
    ])
    if len(all_by_name) > 1:
        failures.append(
            f"{ATTENDEE_NAME} was registered on {len(all_by_name)} events, "
            f"expected only the target event"
        )

    return failures
