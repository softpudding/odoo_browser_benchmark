"""Postcondition checks for event_product.create_event_product_link_to_ticket."""

EVENT_NAME = "Spring Summit"
PRODUCT_NAME = "Conference Pass Std"
TICKET_NAME = "Standard Pass"
TICKET_PRICE = 100.0
TICKET_SEATS_MAX = 200
PRODUCT_PRICE = 100.0


def check(env):
    failures = []

    # ---- Product ----
    products = env["product.product"].search([("name", "=", PRODUCT_NAME)])
    if len(products) != 1:
        failures.append(
            f"Expected exactly 1 product named '{PRODUCT_NAME}', "
            f"found {len(products)}"
        )
        return failures
    product = products[0]

    if product.type != "service":
        failures.append(
            f"Product type is '{product.type}', expected 'service'"
        )
    if abs(product.list_price - PRODUCT_PRICE) > 0.0001:
        failures.append(
            f"Product list_price is {product.list_price}, expected "
            f"{PRODUCT_PRICE}"
        )
    if product.service_tracking != "event":
        failures.append(
            f"Product service_tracking is '{product.service_tracking}', "
            "expected 'event' (the 'Event Registration' option must be "
            "selected so the product can be used on an event ticket)"
        )

    # ---- Event + ticket ----
    events = env["event.event"].search([("name", "=", EVENT_NAME)])
    if len(events) != 1:
        failures.append(
            f"Expected exactly 1 event named '{EVENT_NAME}', "
            f"found {len(events)}"
        )
        return failures
    event = events[0]

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
            f"{TICKET_SEATS_MAX}"
        )
    if not ticket.product_id or ticket.product_id != product:
        actual = ticket.product_id.name if ticket.product_id else None
        failures.append(
            f"Ticket product is '{actual}', expected '{PRODUCT_NAME}' "
            "(the new ticket must be linked to the seeded product)"
        )

    # No extra non-placeholder ticket on the event.
    extra_tickets = (event.event_ticket_ids - tickets).filtered(
        lambda t: not (t.name or "").startswith("Registration for ")
    )
    if extra_tickets:
        failures.append(
            f"Found {len(extra_tickets)} extra ticket(s) on the event: "
            f"{extra_tickets.mapped('name')}"
        )

    # No registrations expected.
    regs = env["event.registration"].search([("event_id", "=", event.id)])
    if regs:
        failures.append(
            f"Expected 0 registrations on '{EVENT_NAME}', found "
            f"{len(regs)} (this task does not require attendee creation)"
        )

    # The event itself must not have been renamed / re-dated. We assume
    # the seed dates as canonical.
    if event.name != EVENT_NAME:
        failures.append(
            f"Event name is '{event.name}', expected '{EVENT_NAME}'"
        )

    return failures
