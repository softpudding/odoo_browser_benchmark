"""Postcondition checks for event.create_event_configure_ticket."""


EVENT_NAME = "Spring Tech Conference 2026"
TICKET_NAME = "Standard Pass"
VENUE_NAME = "Riverside Convention Center"


def check(env):
    failures = []

    events = env["event.event"].search([("name", "=", EVENT_NAME)])
    if len(events) != 1:
        return [f"Expected exactly 1 event named '{EVENT_NAME}', found {len(events)}"]

    event = events[0]

    # Verify date span covers 2026-04-15 and ends on 2026-04-16 (tz-independent
    # check — we assert the calendar dates rather than exact UTC time so the
    # test stays stable across TZ conversions).
    if event.date_begin is False or event.date_end is False:
        failures.append("Event dates not set")
    else:
        begin_date_str = str(event.date_begin)[:10]
        end_date_str = str(event.date_end)[:10]
        if begin_date_str != "2026-04-15":
            failures.append(
                f"Event start date is '{begin_date_str}', expected '2026-04-15'"
            )
        if end_date_str != "2026-04-16":
            failures.append(
                f"Event end date is '{end_date_str}', expected '2026-04-16'"
            )

    # Verify venue (address_id).
    if not event.address_id:
        failures.append("Event venue (Location) is not set")
    elif event.address_id.name != VENUE_NAME:
        failures.append(
            f"Event venue is '{event.address_id.name}', expected '{VENUE_NAME}'"
        )

    tickets = event.event_ticket_ids.filtered(lambda t: t.name == TICKET_NAME)
    if len(tickets) != 1:
        failures.append(
            f"Expected exactly 1 ticket named '{TICKET_NAME}', found {len(tickets)}"
        )
        return failures

    ticket = tickets[0]
    if abs(ticket.price - 150.0) > 0.0001:
        failures.append(f"Ticket price is {ticket.price}, expected 150.0")
    if not ticket.seats_limited:
        failures.append("Ticket seat limit is not enabled")
    if ticket.seats_max != 100:
        failures.append(f"Ticket seat limit is {ticket.seats_max}, expected 100")

    return failures
