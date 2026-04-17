"""Cleanup for event.set_ticket_seat_availability_limit."""

EVENT_NAME = "Autumn AI Summit"


def cleanup(env):
    event = env["event.event"].search([("name", "=", EVENT_NAME)], limit=1)
    if event:
        event.event_ticket_ids.unlink()
        event.unlink()
