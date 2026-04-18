"""Postcondition checks for event_sale.add_seat_limited_ticket_register_until_full."""

EVENT_NAME = "Spring Q2 Workshop"
TICKET_NAME = "VIP Seat"
TICKET_PRICE = 200.0
TICKET_SEATS_MAX = 5
EXPECTED_NAMES = [f"VIP-{i}" for i in range(1, 6)]  # VIP-1..VIP-5
FORBIDDEN_NAME = "VIP-6"


def check(env):
    failures = []

    events = env["event.event"].search([("name", "=", EVENT_NAME)])
    if len(events) != 1:
        return [
            f"Expected exactly 1 event named '{EVENT_NAME}', found {len(events)}"
        ]
    event = events[0]

    # ---- VIP Seat ticket ----
    tickets = event.event_ticket_ids.filtered(
        lambda t: t.name == TICKET_NAME
    )
    if len(tickets) != 1:
        failures.append(
            f"Expected exactly 1 '{TICKET_NAME}' ticket on '{EVENT_NAME}', "
            f"found {len(tickets)}"
        )
        return failures
    ticket = tickets[0]

    if abs(ticket.price - TICKET_PRICE) > 0.0001:
        failures.append(
            f"Ticket price is {ticket.price}, expected {TICKET_PRICE}"
        )
    if ticket.seats_max != TICKET_SEATS_MAX:
        failures.append(
            f"Ticket seats_max is {ticket.seats_max}, expected "
            f"{TICKET_SEATS_MAX} (the agent must NOT raise the cap to "
            "fit a 6th attendee)"
        )

    # No extra named tickets besides the auto-default placeholder
    # ('Registration for ...').
    extra_tickets = (event.event_ticket_ids - tickets).filtered(
        lambda t: not (t.name or "").startswith("Registration for ")
    )
    if extra_tickets:
        failures.append(
            f"Found {len(extra_tickets)} unexpected ticket(s) on the "
            f"event: {extra_tickets.mapped('name')}"
        )

    # ---- The 5 registrations on the event ----
    regs = env["event.registration"].search([
        ("event_id", "=", event.id),
        ("name", "in", EXPECTED_NAMES),
    ])
    found_names = sorted(regs.mapped("name"))
    if found_names != sorted(EXPECTED_NAMES):
        failures.append(
            f"Expected the 5 registrations {EXPECTED_NAMES} on "
            f"'{EVENT_NAME}'; found {found_names}"
        )
        return failures

    if len(regs) != len(EXPECTED_NAMES):
        failures.append(
            f"Expected exactly 5 VIP registrations, found {len(regs)}"
        )

    for reg in regs:
        if reg.state != "open":
            failures.append(
                f"Registration '{reg.name}' state is '{reg.state}', "
                "expected 'open' (Registered)"
            )
        if not reg.event_ticket_id or reg.event_ticket_id != ticket:
            actual = (
                reg.event_ticket_id.name if reg.event_ticket_id else None
            )
            failures.append(
                f"Registration '{reg.name}' is on ticket '{actual}', "
                f"expected '{TICKET_NAME}'"
            )

    # ---- No VIP-6 anywhere ----
    forbidden_regs = env["event.registration"].with_context(
        active_test=False
    ).search([("name", "=", FORBIDDEN_NAME)])
    if forbidden_regs:
        failures.append(
            f"Found {len(forbidden_regs)} registration(s) named "
            f"'{FORBIDDEN_NAME}' — the seat-limit must have blocked "
            "the 6th attendee from being created."
        )

    # ---- No extra registrations on the event ----
    all_event_regs = env["event.registration"].search(
        [("event_id", "=", event.id)]
    )
    extras = all_event_regs - regs
    if extras:
        failures.append(
            f"Found {len(extras)} unexpected registration(s) on "
            f"'{EVENT_NAME}': {extras.mapped('name')}"
        )

    return failures
