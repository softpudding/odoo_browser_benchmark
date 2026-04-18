"""Cleanup for event_product.sell_event_product_fill_attendee_details."""

EVENT_NAME = "Bench Summit"
PARTNER_NAME = "Bench Attendee Co"
PRODUCT_NAME = "Bench Summit Ticket"
ATTENDEE_NAME = "Alice Attendee"


def cleanup(env):
    partner = env["res.partner"].with_context(active_test=False).search(
        [("name", "=", PARTNER_NAME)], limit=1
    )
    if partner:
        orders = env["sale.order"].with_context(active_test=False).search(
            [("partner_id", "=", partner.id)]
        )
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

    env["event.registration"].with_context(active_test=False).search(
        [("name", "=", ATTENDEE_NAME)]
    ).unlink()

    events = env["event.event"].with_context(active_test=False).search(
        [("name", "=", EVENT_NAME)]
    )
    if events:
        regs = env["event.registration"].with_context(
            active_test=False
        ).search([("event_id", "in", events.ids)])
        if regs:
            regs.unlink()
        events.mapped("event_ticket_ids").unlink()
        events.unlink()

    products = env["product.product"].with_context(active_test=False).search(
        [("name", "=", PRODUCT_NAME)]
    )
    if products:
        tickets = env["event.event.ticket"].with_context(
            active_test=False
        ).search([("product_id", "in", products.ids)])
        if tickets:
            regs = env["event.registration"].with_context(
                active_test=False
            ).search([("event_ticket_id", "in", tickets.ids)])
            if regs:
                regs.unlink()
            tickets.unlink()
        templates = products.mapped("product_tmpl_id")
        try:
            products.unlink()
        except Exception:
            pass
        try:
            templates.unlink()
        except Exception:
            pass
