"""Seed for event.set_ticket_seat_availability_limit."""

EVENT_NAME = "Autumn AI Summit"
TICKET_NAME = "General Admission"


def setup(env):
    event = env["event.event"].search([("name", "=", EVENT_NAME)], limit=1)
    values = {
        "name": EVENT_NAME,
        "date_begin": "2026-10-05 09:00:00",
        "date_end": "2026-10-07 17:00:00",
    }
    if not event:
        event = env["event.event"].create(values)
    else:
        event.write(values)

    env.flush_all()
    # Remove all existing tickets then add a single General Admission
    # ticket with seats_max=100 so the seed state is deterministic.
    env["event.event.ticket"].search([("event_id", "=", event.id)]).unlink()
    env["event.event.ticket"].create({
        "event_id": event.id,
        "name": TICKET_NAME,
        "price": 50.0,
        "seats_max": 100,
    })
