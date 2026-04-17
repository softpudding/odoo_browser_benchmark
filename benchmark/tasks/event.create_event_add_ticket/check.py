"""Postcondition checks for event.create_event_add_ticket."""


EVENT_NAME = "Operations Leadership Summit 2026"
TICKET_NAME = "Standard Pass"


def check(env):
    failures = []

    events = env["event.event"].search([("name", "=", EVENT_NAME)])
    if len(events) != 1:
        return [f"Expected exactly 1 event named '{EVENT_NAME}', found {len(events)}"]

    event = events[0]
    if str(event.date_begin) != "2026-07-10 01:00:00":
        failures.append(f"Event start is '{event.date_begin}', expected '2026-07-10 01:00:00'")
    if str(event.date_end) != "2026-07-10 08:30:00":
        failures.append(f"Event end is '{event.date_end}', expected '2026-07-10 08:30:00'")
    if not event.seats_limited:
        failures.append("Event attendee limit is not enabled")
    if event.seats_max != 60:
        failures.append(f"Event attendee limit is {event.seats_max}, expected 60")

    tickets = event.event_ticket_ids.filtered(lambda ticket: ticket.name == TICKET_NAME)
    if len(tickets) != 1:
        failures.append(f"Expected exactly 1 ticket named '{TICKET_NAME}', found {len(tickets)}")
        return failures

    ticket = tickets[0]
    if abs(ticket.price - 199.0) > 0.0001:
        failures.append(f"Ticket price is {ticket.price}, expected 199.0")
    if not ticket.seats_limited:
        failures.append("Ticket seat limit is not enabled")
    if ticket.seats_max != 50:
        failures.append(f"Ticket seat limit is {ticket.seats_max}, expected 50")

    return failures
