"""Postcondition checks for event_product.sell_event_product_fill_attendee_details."""

EVENT_NAME = "Bench Festival 2026"
TICKET_NAME = "Standard"
PRODUCT_NAME = "Bench Standard Ticket"
PARTNER_NAME = "Bench Attendee Customer"
ATTENDEE_NAME = "Bench Attendee Name"
ATTENDEE_EMAIL = "bench.attendee@example.com"


def check(env):
    failures = []

    # ---- Event + ticket (seed sanity) ----
    events = env["event.event"].search([("name", "=", EVENT_NAME)])
    if len(events) != 1:
        return [
            f"Expected exactly 1 event named '{EVENT_NAME}', found {len(events)}"
        ]
    event = events[0]

    tickets = event.event_ticket_ids.filtered(
        lambda t: t.name == TICKET_NAME
    )
    if len(tickets) != 1:
        return [
            f"Expected exactly 1 '{TICKET_NAME}' ticket on '{EVENT_NAME}', "
            f"found {len(tickets)}"
        ]
    ticket = tickets[0]
    if not ticket.product_id or ticket.product_id.name != PRODUCT_NAME:
        failures.append(
            f"Ticket product is "
            f"'{ticket.product_id.name if ticket.product_id else None}', "
            f"expected '{PRODUCT_NAME}' (seed broken)"
        )

    # ---- Partner ----
    partner = env["res.partner"].search(
        [("name", "=", PARTNER_NAME)], limit=1
    )
    if not partner:
        return [f"Partner '{PARTNER_NAME}' not found (seed broken)"]

    # ---- Sales order ----
    orders = env["sale.order"].search([("partner_id", "=", partner.id)])
    if len(orders) != 1:
        failures.append(
            f"Expected exactly 1 sale.order for '{PARTNER_NAME}', "
            f"found {len(orders)}"
        )
        return failures
    order = orders[0]

    if order.state not in ("sale", "done"):
        failures.append(
            f"Sales order state is '{order.state}', expected 'sale' or 'done'"
        )

    event_lines = order.order_line.filtered(lambda line: line.event_id == event)
    if len(event_lines) != 1:
        failures.append(
            f"Expected 1 event-related order line, found {len(event_lines)}"
        )
        return failures
    line = event_lines[0]
    if line.event_ticket_id != ticket:
        failures.append(
            f"Order line ticket is "
            f"'{line.event_ticket_id.name if line.event_ticket_id else None}', "
            f"expected '{TICKET_NAME}'"
        )
    if line.product_id != ticket.product_id:
        failures.append(
            f"Order line product is "
            f"'{line.product_id.name if line.product_id else None}', "
            f"expected '{PRODUCT_NAME}'"
        )
    if abs(line.product_uom_qty - 1.0) > 0.0001:
        failures.append(
            f"Order line quantity is {line.product_uom_qty}, expected 1"
        )

    # ---- Registration ----
    regs = env["event.registration"].search([
        ("event_id", "=", event.id),
        ("event_ticket_id", "=", ticket.id),
    ])
    if len(regs) != 1:
        failures.append(
            f"Expected exactly 1 registration for '{TICKET_NAME}' on "
            f"'{EVENT_NAME}', found {len(regs)}"
        )
        return failures
    reg = regs[0]

    if reg.state != "open":
        failures.append(
            f"Registration state is '{reg.state}', expected 'open' (Registered)"
        )

    if (reg.name or "").strip() != ATTENDEE_NAME:
        failures.append(
            f"Registration attendee name is '{reg.name}', "
            f"expected '{ATTENDEE_NAME}'"
        )

    if (reg.email or "").strip().lower() != ATTENDEE_EMAIL:
        failures.append(
            f"Registration email is '{reg.email}', "
            f"expected '{ATTENDEE_EMAIL}'"
        )

    if reg.sale_order_id != order:
        failures.append(
            f"Registration sale_order is "
            f"'{reg.sale_order_id.name if reg.sale_order_id else None}', "
            f"expected '{order.name}'"
        )

    # No extra registrations named with the attendee on other events.
    extra_regs = env["event.registration"].search([
        ("name", "=", ATTENDEE_NAME),
    ]) - reg
    if extra_regs:
        failures.append(
            f"Found {len(extra_regs)} extra registration(s) named "
            f"'{ATTENDEE_NAME}'"
        )

    return failures
