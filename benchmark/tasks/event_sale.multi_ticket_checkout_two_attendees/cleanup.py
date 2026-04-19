"""Cleanup for event_sale.multi_ticket_checkout_two_attendees."""

EVENT_NAME = "Bench Summit 2026"
PARTNER_NAME = "Bench Summit Customer"
ATTENDEE_EARLY_NAME = "Alice Summit Attendee"
ATTENDEE_VIP_NAME = "Bob Summit Attendee"


def cleanup(env):
    partner = env["res.partner"].search(
        [("name", "=", PARTNER_NAME)], limit=1
    )
    if partner:
        orders = env["sale.order"].search([("partner_id", "=", partner.id)])
        for order in orders:
            if order.state == "sale":
                try:
                    order.action_cancel()
                except Exception:
                    pass
            try:
                order.unlink()
            except Exception:
                pass

    # Remove any registrations still named for our attendees.
    env["event.registration"].search([
        ("name", "in", [ATTENDEE_EARLY_NAME, ATTENDEE_VIP_NAME]),
    ]).unlink()

    events = env["event.event"].search([("name", "=", EVENT_NAME)])
    if events:
        regs = env["event.registration"].search(
            [("event_id", "in", events.ids)]
        )
        if regs:
            try:
                regs.unlink()
            except Exception:
                pass
        try:
            events.mapped("event_ticket_ids").unlink()
        except Exception:
            pass
        try:
            events.unlink()
        except Exception:
            pass
