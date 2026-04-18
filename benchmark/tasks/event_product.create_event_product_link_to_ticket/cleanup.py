"""Cleanup for event_product.create_event_product_link_to_ticket."""

EVENT_NAME = "Spring Summit"
PRODUCT_NAME = "Conference Pass Std"


def cleanup(env):
    # Drop tickets/registrations linked to our product first.
    products = env["product.product"].with_context(active_test=False).search(
        [("name", "=", PRODUCT_NAME)]
    )

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
