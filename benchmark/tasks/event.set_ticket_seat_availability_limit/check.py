"""Postcondition checks for event.set_ticket_seat_availability_limit."""


EVENT_NAME = "Autumn AI Summit"
TICKET_NAME = "General Admission"
EXPECTED_SEATS_MAX = 250


def check(env):
    failures = []
    event = env["event.event"].search([("name", "=", EVENT_NAME)], limit=1)
    if not event:
        return [f"Event '{EVENT_NAME}' not found"]

    tickets = event.event_ticket_ids.filtered(
        lambda t: t.name == TICKET_NAME
    )
    if not tickets:
        return [f"Ticket '{TICKET_NAME}' not found on event"]
    if len(tickets) > 1:
        failures.append(
            f"Found {len(tickets)} '{TICKET_NAME}' tickets, expected 1"
        )

    t = tickets[0]
    if (t.seats_max or 0) != EXPECTED_SEATS_MAX:
        failures.append(
            f"seats_max is {t.seats_max}, expected {EXPECTED_SEATS_MAX}"
        )
    return failures
