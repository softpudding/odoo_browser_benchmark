"""Postcondition checks for event_product.sell_event_product_fill_attendee_details."""


EVENT_NAME = "Partner Enablement Day"
PARTNER_NAME = "Northwind Workshops"
PRODUCT_NAME = "Enablement Seat Product"
TICKET_NAME = "Workshop Seat"
ATTENDEE_NAME = "Jordan Rivera"
ATTENDEE_EMAIL = "jordan.rivera@example.com"


def check(env):
    failures = []

    event = env["event.event"].search([("name", "=", EVENT_NAME)], limit=1)
    if not event:
        return [f"Event '{EVENT_NAME}' not found"]

    ticket = event.event_ticket_ids.filtered(lambda t: t.name == TICKET_NAME)[:1]
    if not ticket:
        return [f"Ticket '{TICKET_NAME}' not found on event '{EVENT_NAME}'"]
    ticket = ticket[0]
    if not ticket.product_id or ticket.product_id.name != PRODUCT_NAME:
        failures.append(
            f"Ticket product is {ticket.product_id.name!r}, expected {PRODUCT_NAME!r}"
        )

    partner = env["res.partner"].search([("name", "=", PARTNER_NAME)], limit=1)
    if not partner:
        return failures + [f"Partner '{PARTNER_NAME}' not found"]

    orders = env["sale.order"].search([
        ("partner_id", "=", partner.id),
        ("order_line.event_id", "=", event.id),
    ])
    if len(orders) != 1:
        failures.append(
            f"Expected exactly 1 sale order for '{PARTNER_NAME}' on '{EVENT_NAME}', found {len(orders)}"
        )
        return failures
    order = orders[0]
    if order.state not in ("sale", "done"):
        failures.append(f"Sale order state is {order.state!r}, expected 'sale'")
    if abs(order.amount_total - 95.0) > 0.01:
        failures.append(f"Sale order total is {order.amount_total}, expected 95.0")

    lines = order.order_line.filtered(lambda l: l.product_id.name == PRODUCT_NAME)
    if len(lines) != 1:
        failures.append(
            f"Expected exactly 1 order line for {PRODUCT_NAME!r}, found {len(lines)}"
        )
    else:
        line = lines[0]
        if abs(line.product_uom_qty - 1.0) > 0.0001:
            failures.append(f"Order line quantity is {line.product_uom_qty}, expected 1")
        if line.event_ticket_id != ticket:
            failures.append(
                f"Order line ticket is {line.event_ticket_id.name!r}, expected {TICKET_NAME!r}"
            )

    regs = env["event.registration"].search([
        ("event_id", "=", event.id),
        ("name", "=", ATTENDEE_NAME),
    ])
    if len(regs) != 1:
        failures.append(
            f"Expected exactly 1 registration for '{ATTENDEE_NAME}', found {len(regs)}"
        )
        return failures
    reg = regs[0]
    if reg.state != "open":
        failures.append(f"Registration state is {reg.state!r}, expected 'open'")
    if (reg.email or "").strip().lower() != ATTENDEE_EMAIL:
        failures.append(
            f"Registration email is {reg.email!r}, expected {ATTENDEE_EMAIL!r}"
        )
    if reg.event_ticket_id != ticket:
        failures.append(
            f"Registration ticket is {reg.event_ticket_id.name!r}, expected {TICKET_NAME!r}"
        )
    if reg.sale_order_id != order:
        failures.append("Registration is not linked to the created sale order")

    extra_regs = env["event.registration"].search([
        ("event_id", "=", event.id),
    ]) - reg
    if extra_regs:
        failures.append(
            f"Found {len(extra_regs)} extra registration(s) on '{EVENT_NAME}'"
        )

    invoices = env["account.move"].search([
        ("partner_id", "=", partner.id),
        ("move_type", "=", "out_invoice"),
    ])
    if invoices:
        failures.append("No invoice should be created for this task")

    return failures
