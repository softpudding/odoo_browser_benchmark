"""Seed for event.register_attendee_confirm_check_in.

Creates the Product Update Q2 event. Task: register Sofia Reyes,
confirm, and check her in.
"""

EVENT_NAME = "Product Update Q2 — Partners Meetup"
ATTENDEE_NAME = "Sofia Reyes"


def setup(env):
    # Cleanup prior registrations (any event with same attendee name).
    env["event.registration"].search([("name", "=", ATTENDEE_NAME)]).unlink()

    event = env["event.event"].search([("name", "=", EVENT_NAME)], limit=1)
    values = {
        "name": EVENT_NAME,
        "date_begin": "2026-06-18 09:00:00",
        "date_end": "2026-06-18 17:00:00",
    }
    if not event:
        event = env["event.event"].create(values)
    else:
        event.write(values)
        # Remove prior registrations for this event with our attendee name.
        env["event.registration"].search([
            ("event_id", "=", event.id),
            ("name", "=", ATTENDEE_NAME),
        ]).unlink()
