"""Postcondition checks for event_sale.multi_ticket_checkout_two_attendees."""

EVENT_NAME = "Bench Summit 2026"
TICKET_EARLY = "Early Bird"
TICKET_VIP = "VIP"
PRODUCT_EARLY = "Bench Summit Early Bird Ticket"
PRODUCT_VIP = "Bench Summit VIP Ticket"
PARTNER_NAME = "Bench Summit Customer"

ATTENDEE_EARLY_NAME = "Alice Summit Attendee"
ATTENDEE_EARLY_EMAIL = "alice.summit@example.com"
ATTENDEE_VIP_NAME = "Bob Summit Attendee"
ATTENDEE_VIP_EMAIL = "bob.summit@example.com"

EXPECTED_AMOUNT_TOTAL = 600.0


def check(env):
    failures = []

    # ---- Event + tickets (seed sanity) ----
    events = env["event.event"].search([("name", "=", EVENT_NAME)])
    if len(events) != 1:
        return [
            f"Expected exactly 1 event named '{EVENT_NAME}', found {len(events)}"
        ]
    event = events[0]

    early_tickets = event.event_ticket_ids.filtered(
        lambda t: t.name == TICKET_EARLY
    )
    vip_tickets = event.event_ticket_ids.filtered(
        lambda t: t.name == TICKET_VIP
    )
    if len(early_tickets) != 1:
        return [
            f"Expected exactly 1 '{TICKET_EARLY}' ticket on '{EVENT_NAME}', "
            f"found {len(early_tickets)}"
        ]
    if len(vip_tickets) != 1:
        return [
            f"Expected exactly 1 '{TICKET_VIP}' ticket on '{EVENT_NAME}', "
            f"found {len(vip_tickets)}"
        ]
    early_ticket = early_tickets[0]
    vip_ticket = vip_tickets[0]

    if not early_ticket.product_id or early_ticket.product_id.name != PRODUCT_EARLY:
        failures.append(
            f"Early Bird ticket product is "
            f"'{early_ticket.product_id.name if early_ticket.product_id else None}', "
            f"expected '{PRODUCT_EARLY}' (seed broken)"
        )
    if not vip_ticket.product_id or vip_ticket.product_id.name != PRODUCT_VIP:
        failures.append(
            f"VIP ticket product is "
            f"'{vip_ticket.product_id.name if vip_ticket.product_id else None}', "
            f"expected '{PRODUCT_VIP}' (seed broken)"
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
    if len(event_lines) != 2:
        failures.append(
            f"Expected 2 event-related order lines, found {len(event_lines)}"
        )
        return failures

    early_lines = event_lines.filtered(
        lambda l: l.event_ticket_id == early_ticket
    )
    vip_lines = event_lines.filtered(
        lambda l: l.event_ticket_id == vip_ticket
    )
    if len(early_lines) != 1:
        failures.append(
            f"Expected 1 order line for '{TICKET_EARLY}' ticket, "
            f"found {len(early_lines)}"
        )
    if len(vip_lines) != 1:
        failures.append(
            f"Expected 1 order line for '{TICKET_VIP}' ticket, "
            f"found {len(vip_lines)}"
        )
    if early_lines:
        el = early_lines[0]
        if el.product_id.name != PRODUCT_EARLY:
            failures.append(
                f"Early Bird line product is '{el.product_id.name}', "
                f"expected '{PRODUCT_EARLY}'"
            )
        if abs(el.product_uom_qty - 1.0) > 0.0001:
            failures.append(
                f"Early Bird line quantity is {el.product_uom_qty}, expected 1"
            )
    if vip_lines:
        vl = vip_lines[0]
        if vl.product_id.name != PRODUCT_VIP:
            failures.append(
                f"VIP line product is '{vl.product_id.name}', "
                f"expected '{PRODUCT_VIP}'"
            )
        if abs(vl.product_uom_qty - 1.0) > 0.0001:
            failures.append(
                f"VIP line quantity is {vl.product_uom_qty}, expected 1"
            )

    if abs(order.amount_total - EXPECTED_AMOUNT_TOTAL) > 0.01:
        failures.append(
            f"Sale order amount_total is {order.amount_total}, "
            f"expected {EXPECTED_AMOUNT_TOTAL}"
        )

    # ---- Registrations ----
    regs = env["event.registration"].search([
        ("event_id", "=", event.id),
        ("sale_order_id", "=", order.id),
    ])
    if len(regs) != 2:
        failures.append(
            f"Expected exactly 2 registrations on '{EVENT_NAME}' linked to "
            f"the SO, found {len(regs)}"
        )
        return failures

    early_regs = regs.filtered(lambda r: r.event_ticket_id == early_ticket)
    vip_regs = regs.filtered(lambda r: r.event_ticket_id == vip_ticket)
    if len(early_regs) != 1:
        failures.append(
            f"Expected 1 registration for '{TICKET_EARLY}' ticket, "
            f"found {len(early_regs)}"
        )
    if len(vip_regs) != 1:
        failures.append(
            f"Expected 1 registration for '{TICKET_VIP}' ticket, "
            f"found {len(vip_regs)}"
        )

    if early_regs:
        r = early_regs[0]
        if r.state != "open":
            failures.append(
                f"Early Bird registration state is '{r.state}', "
                f"expected 'open' (Registered)"
            )
        if (r.name or "").strip() != ATTENDEE_EARLY_NAME:
            failures.append(
                f"Early Bird registration attendee name is '{r.name}', "
                f"expected '{ATTENDEE_EARLY_NAME}'"
            )
        if (r.email or "").strip().lower() != ATTENDEE_EARLY_EMAIL:
            failures.append(
                f"Early Bird registration email is '{r.email}', "
                f"expected '{ATTENDEE_EARLY_EMAIL}'"
            )

    if vip_regs:
        r = vip_regs[0]
        if r.state != "open":
            failures.append(
                f"VIP registration state is '{r.state}', "
                f"expected 'open' (Registered)"
            )
        if (r.name or "").strip() != ATTENDEE_VIP_NAME:
            failures.append(
                f"VIP registration attendee name is '{r.name}', "
                f"expected '{ATTENDEE_VIP_NAME}'"
            )
        if (r.email or "").strip().lower() != ATTENDEE_VIP_EMAIL:
            failures.append(
                f"VIP registration email is '{r.email}', "
                f"expected '{ATTENDEE_VIP_EMAIL}'"
            )

    # No extra registrations named for our attendees on other events.
    extra_regs = env["event.registration"].search([
        ("name", "in", [ATTENDEE_EARLY_NAME, ATTENDEE_VIP_NAME]),
    ]) - regs
    if extra_regs:
        failures.append(
            f"Found {len(extra_regs)} extra registration(s) with the "
            f"seeded attendee names on other events/orders"
        )

    return failures
