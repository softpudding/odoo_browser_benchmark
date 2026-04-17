"""Postcondition checks for event.create_event_add_ticket.

Validates:
1. An event "Odoo Community Days 2026" exists.
2. Event has dates in July 2026.
3. Event has a ticket named "Standard Pass" with price 75.00 and seats 200.
"""

EVENT_NAME = "Odoo Community Days 2026"


def check(env):
    failures = []

    event = env["event.event"].search([("name", "=", EVENT_NAME)], limit=1)
    if not event:
        return [f"Event '{EVENT_NAME}' not found"]

    # Check dates are in July 2026
    if event.date_begin:
        if event.date_begin.year != 2026 or event.date_begin.month != 7:
            failures.append(
                f"Event start date is {event.date_begin}, expected July 2026"
            )
    else:
        failures.append("Event has no start date")

    if event.date_end:
        if event.date_end.year != 2026 or event.date_end.month != 7:
            failures.append(
                f"Event end date is {event.date_end}, expected July 2026"
            )
    else:
        failures.append("Event has no end date")

    # Check ticket
    tickets = event.event_ticket_ids
    if not tickets:
        failures.append("Event has no tickets")
    else:
        standard = tickets.filtered(lambda t: t.name == "Standard Pass")
        if not standard:
            ticket_names = [t.name for t in tickets]
            failures.append(
                f"No ticket named 'Standard Pass'; found: {ticket_names}"
            )
        else:
            ticket = standard[0]
            if abs(ticket.price - 75.0) > 0.01:
                failures.append(
                    f"Ticket price is {ticket.price}, expected 75.00"
                )
            if ticket.seats_max != 200:
                failures.append(
                    f"Ticket max seats is {ticket.seats_max}, expected 200"
                )

    return failures
