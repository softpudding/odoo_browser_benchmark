"""Postcondition checks for event_sale.multi_ticket_checkout_two_attendees.

Verifies the end state of the multi-ticket public checkout:
- One sale.order in state 'sale' (or 'done'), amount_total = 200.0,
  with exactly two event-ticket lines (Standard + VIP).
- Two event.registration records linked to that SO, one per ticket,
  with the correct attendee name/email.
"""

EVENT_NAME = "Bench Expo 2026"
TICKET_STANDARD = "Standard"
TICKET_VIP = "VIP"
PRICE_STANDARD = 50.0
PRICE_VIP = 150.0
PRODUCT_STANDARD = "Bench Expo Standard Pass"
PRODUCT_VIP = "Bench Expo VIP Pass"
EXPECTED_TOTAL = 200.0

ATTENDEE_STANDARD_NAME = "Alice Standard"
ATTENDEE_STANDARD_EMAIL = "alice@benchexpo.test"
ATTENDEE_VIP_NAME = "Bob VIP"
ATTENDEE_VIP_EMAIL = "bob@benchexpo.test"


def check(env):
    failures = []

    events = env["event.event"].with_context(active_test=False).search([
        ("name", "=", EVENT_NAME),
    ])
    if not events:
        return [f"Seed broken: no event named '{EVENT_NAME}'"]
    if len(events) != 1:
        failures.append(
            f"Expected exactly 1 event named '{EVENT_NAME}', found {len(events)}"
        )
    event = events[0]

    tickets = {t.name: t for t in event.event_ticket_ids}
    if TICKET_STANDARD not in tickets:
        return [f"Seed broken: no '{TICKET_STANDARD}' ticket on '{EVENT_NAME}'"]
    if TICKET_VIP not in tickets:
        return [f"Seed broken: no '{TICKET_VIP}' ticket on '{EVENT_NAME}'"]

    ticket_std = tickets[TICKET_STANDARD]
    ticket_vip = tickets[TICKET_VIP]

    # ----- Registrations -----
    regs = env["event.registration"].with_context(active_test=False).search([
        ("event_id", "=", event.id),
    ])
    # Only count non-cancelled registrations for the attendee assertions.
    live_regs = regs.filtered(lambda r: r.state != "cancel")
    if len(live_regs) != 2:
        failures.append(
            f"Expected exactly 2 (non-cancelled) registrations on "
            f"'{EVENT_NAME}', found {len(live_regs)}"
        )

    by_name = {r.name: r for r in live_regs}
    reg_std = by_name.get(ATTENDEE_STANDARD_NAME)
    reg_vip = by_name.get(ATTENDEE_VIP_NAME)

    if not reg_std:
        failures.append(
            f"No registration named '{ATTENDEE_STANDARD_NAME}' on '{EVENT_NAME}'"
        )
    else:
        if (reg_std.email or "").strip().lower() != ATTENDEE_STANDARD_EMAIL.lower():
            failures.append(
                f"Standard registration email is {reg_std.email!r}, "
                f"expected {ATTENDEE_STANDARD_EMAIL!r}"
            )
        if reg_std.event_ticket_id != ticket_std:
            failures.append(
                f"'{ATTENDEE_STANDARD_NAME}' is linked to ticket "
                f"{reg_std.event_ticket_id.name!r}, expected "
                f"{TICKET_STANDARD!r}"
            )

    if not reg_vip:
        failures.append(
            f"No registration named '{ATTENDEE_VIP_NAME}' on '{EVENT_NAME}'"
        )
    else:
        if (reg_vip.email or "").strip().lower() != ATTENDEE_VIP_EMAIL.lower():
            failures.append(
                f"VIP registration email is {reg_vip.email!r}, "
                f"expected {ATTENDEE_VIP_EMAIL!r}"
            )
        if reg_vip.event_ticket_id != ticket_vip:
            failures.append(
                f"'{ATTENDEE_VIP_NAME}' is linked to ticket "
                f"{reg_vip.event_ticket_id.name!r}, expected "
                f"{TICKET_VIP!r}"
            )

    # Both registrations should belong to the same confirmed SO.
    if reg_std and reg_vip:
        if not reg_std.sale_order_id:
            failures.append("Standard registration is not linked to a sale order")
        if not reg_vip.sale_order_id:
            failures.append("VIP registration is not linked to a sale order")
        if reg_std.sale_order_id and reg_vip.sale_order_id \
                and reg_std.sale_order_id != reg_vip.sale_order_id:
            failures.append(
                f"Standard and VIP registrations are on different sale orders: "
                f"{reg_std.sale_order_id.name!r} vs {reg_vip.sale_order_id.name!r}"
            )

    # ----- Sale order -----
    order = reg_std.sale_order_id if reg_std else (
        reg_vip.sale_order_id if reg_vip else env["sale.order"].browse()
    )

    if not order:
        failures.append("Could not locate the sale order via the registrations")
        return failures

    # Wire Transfer transitions the payment.transaction to 'pending'
    # (not 'done'), which triggers `action_quotation_sent` on the SO
    # via the sale payment-transaction post-process.  The SO ends up in
    # state 'sent', not 'sale'.  Accept either 'sent' or 'sale'/'done'
    # so a later manual confirmation of the wire transfer doesn't cause
    # false positives.
    if order.state not in ("sent", "sale", "done"):
        failures.append(
            f"Sale order state is {order.state!r}, expected "
            f"'sent', 'sale' or 'done'"
        )

    # Also assert that a payment.transaction was created for this SO
    # (in state 'pending' or 'done').  This is the signal that the
    # agent actually went through /shop/payment and submitted the
    # Wire Transfer option.
    txs = env["payment.transaction"].search([
        ("sale_order_ids", "in", order.id),
    ])
    if not txs:
        failures.append(
            f"No payment.transaction linked to sale order {order.name!r}"
        )
    else:
        tx_states = txs.mapped("state")
        if not any(s in ("pending", "authorized", "done") for s in tx_states):
            failures.append(
                f"Payment transaction state(s) are {tx_states}, "
                f"expected at least one in ('pending','authorized','done')"
            )
        # Must be the Wire Transfer provider.
        wire = env.ref(
            "payment.payment_provider_transfer", raise_if_not_found=False
        )
        if wire and not any(t.provider_id == wire for t in txs):
            failures.append(
                "No transaction uses the 'Wire Transfer' payment "
                "provider — agent likely paid with a different method"
            )

    # Exactly 2 event-ticket lines; ignore any non-event (e.g., delivery) lines.
    event_lines = order.order_line.filtered(
        lambda line: line.event_id == event and line.event_ticket_id
    )
    if len(event_lines) != 2:
        failures.append(
            f"Expected exactly 2 event-related order lines, "
            f"found {len(event_lines)}"
        )

    ticket_to_line = {l.event_ticket_id: l for l in event_lines}
    line_std = ticket_to_line.get(ticket_std)
    line_vip = ticket_to_line.get(ticket_vip)

    if not line_std:
        failures.append("No order line for the Standard ticket")
    else:
        if abs(line_std.product_uom_qty - 1.0) > 0.001:
            failures.append(
                f"Standard line quantity is {line_std.product_uom_qty}, expected 1"
            )
        if abs(line_std.price_unit - PRICE_STANDARD) > 0.01:
            failures.append(
                f"Standard line unit price is {line_std.price_unit}, "
                f"expected {PRICE_STANDARD}"
            )

    if not line_vip:
        failures.append("No order line for the VIP ticket")
    else:
        if abs(line_vip.product_uom_qty - 1.0) > 0.001:
            failures.append(
                f"VIP line quantity is {line_vip.product_uom_qty}, expected 1"
            )
        if abs(line_vip.price_unit - PRICE_VIP) > 0.01:
            failures.append(
                f"VIP line unit price is {line_vip.price_unit}, "
                f"expected {PRICE_VIP}"
            )

    if abs(order.amount_total - EXPECTED_TOTAL) > 0.01:
        failures.append(
            f"Sale order amount_total is {order.amount_total}, "
            f"expected {EXPECTED_TOTAL}"
        )

    # ----- No sibling orders for the same event -----
    other_orders = env["sale.order"].with_context(active_test=False).search([
        ("order_line.event_id", "=", event.id),
        ("id", "!=", order.id),
        ("state", "in", ("sale", "done", "draft", "sent")),
    ])
    if other_orders:
        failures.append(
            f"Found {len(other_orders)} extra sale order(s) for "
            f"'{EVENT_NAME}' beyond the expected one: "
            f"{other_orders.mapped('name')}"
        )

    # ----- No sibling registrations beyond the two we want -----
    other_regs = live_regs - (reg_std + reg_vip) if (reg_std or reg_vip) else live_regs
    if other_regs:
        failures.append(
            f"Found {len(other_regs)} extra registration(s) on "
            f"'{EVENT_NAME}': {other_regs.mapped('name')}"
        )

    return failures
