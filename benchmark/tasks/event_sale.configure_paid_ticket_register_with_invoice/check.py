"""Postcondition checks for event_sale.configure_paid_ticket_register_with_invoice."""

EVENT_NAME = "Spring Dev Summit 2026"
PARTNER_NAME = "Bench Summit Attendee Inc"
PRODUCT_NAME = "Dev Summit Pro Product"
TICKET_NAME = "Professional Pass"
TICKET_PRICE = 150.0
TICKET_SEATS_MAX = 50
ATTENDEE_NAME = "Berta Attendee"
ATTENDEE_EMAIL = "berta@benchsummit.test"


def check(env):
    failures = []

    # ---- Event + ticket ----
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
            f"Ticket seats_max is {ticket.seats_max}, expected {TICKET_SEATS_MAX}"
        )
    if not ticket.product_id or ticket.product_id.name != PRODUCT_NAME:
        failures.append(
            f"Ticket product is "
            f"'{ticket.product_id.name if ticket.product_id else None}', "
            f"expected '{PRODUCT_NAME}'"
        )

    # Make sure no extra named tickets (the 'Registration for ...' default
    # auto-created on event creation is allowed).
    extra_tickets = (event.event_ticket_ids - tickets).filtered(
        lambda t: not (t.name or "").startswith("Registration for ")
    )
    if extra_tickets:
        failures.append(
            f"Found {len(extra_tickets)} extra ticket(s) on the event: "
            f"{extra_tickets.mapped('name')}"
        )

    # ---- Partner ----
    partner = env["res.partner"].search(
        [("name", "=", PARTNER_NAME)], limit=1
    )
    if not partner:
        failures.append(f"Partner '{PARTNER_NAME}' not found (seed broken)")
        return failures

    # ---- Sales order ----
    orders = env["sale.order"].search([
        ("partner_id", "=", partner.id),
        ("order_line.event_id", "=", event.id),
    ])
    if len(orders) != 1:
        failures.append(
            f"Expected exactly 1 sale.order for '{PARTNER_NAME}' linked to "
            f"event '{EVENT_NAME}', found {len(orders)}"
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
            f"Order line ticket is '{line.event_ticket_id.name}', "
            f"expected '{TICKET_NAME}'"
        )
    if abs(line.product_uom_qty - 1.0) > 0.0001:
        failures.append(
            f"Order line quantity is {line.product_uom_qty}, expected 1"
        )
    if abs(line.price_unit - TICKET_PRICE) > 0.0001:
        failures.append(
            f"Order line unit price is {line.price_unit}, expected {TICKET_PRICE}"
        )

    # ---- Registration ----
    regs = env["event.registration"].search([
        ("event_id", "=", event.id),
        ("name", "=", ATTENDEE_NAME),
    ])
    if len(regs) != 1:
        failures.append(
            f"Expected exactly 1 registration for '{ATTENDEE_NAME}' on "
            f"'{EVENT_NAME}', found {len(regs)}"
        )
        return failures
    reg = regs[0]
    if reg.state != "open":
        failures.append(
            f"Registration state is '{reg.state}', expected 'open' (Registered)"
        )
    if (reg.email or "").strip().lower() != ATTENDEE_EMAIL:
        failures.append(
            f"Registration email is '{reg.email}', expected '{ATTENDEE_EMAIL}'"
        )
    if reg.event_ticket_id != ticket:
        failures.append(
            f"Registration ticket is "
            f"'{reg.event_ticket_id.name if reg.event_ticket_id else None}', "
            f"expected '{TICKET_NAME}'"
        )
    if reg.sale_order_id != order:
        failures.append(
            f"Registration sale_order is "
            f"'{reg.sale_order_id.name if reg.sale_order_id else None}', "
            f"expected '{order.name}'"
        )

    # No other registrations on the event with the same name.
    extra_regs = env["event.registration"].search([
        ("name", "=", ATTENDEE_NAME),
    ]) - reg
    if extra_regs:
        failures.append(
            f"Found {len(extra_regs)} extra registration(s) named "
            f"'{ATTENDEE_NAME}'"
        )

    # ---- Customer invoice (must be DRAFT) ----
    invoices = env["account.move"].search([
        ("partner_id", "=", partner.id),
        ("move_type", "=", "out_invoice"),
    ])
    if len(invoices) != 1:
        failures.append(
            f"Expected exactly 1 customer invoice for '{PARTNER_NAME}', "
            f"found {len(invoices)}"
        )
        return failures
    invoice = invoices[0]

    if invoice.state != "draft":
        failures.append(
            f"Invoice state is '{invoice.state}', expected 'draft' "
            f"(do not post the invoice)"
        )

    # Invoice should be for our SO.
    if order not in invoice.invoice_line_ids.sale_line_ids.order_id:
        failures.append(
            "Invoice is not linked to the expected sales order"
        )

    if abs(invoice.amount_total - TICKET_PRICE) > 0.01:
        failures.append(
            f"Invoice amount_total is {invoice.amount_total}, "
            f"expected {TICKET_PRICE}"
        )
    if abs(invoice.amount_untaxed - TICKET_PRICE) > 0.01:
        failures.append(
            f"Invoice amount_untaxed is {invoice.amount_untaxed}, "
            f"expected {TICKET_PRICE}"
        )

    return failures
