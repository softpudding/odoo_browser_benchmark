"""Cleanup for event_sale.add_seat_limited_ticket_register_until_full."""

EVENT_NAME = "Spring Q2 Workshop"
ATTENDEE_NAMES = [f"VIP-{i}" for i in range(1, 7)]


def cleanup(env):
    # Remove residual VIP-N registrations on any event.
    regs = env["event.registration"].with_context(active_test=False).search(
        [("name", "in", ATTENDEE_NAMES)]
    )
    if regs:
        regs.unlink()

    events = env["event.event"].with_context(active_test=False).search(
        [("name", "=", EVENT_NAME)]
    )
    if events:
        evt_regs = env["event.registration"].with_context(
            active_test=False
        ).search([("event_id", "in", events.ids)])
        if evt_regs:
            evt_regs.unlink()
        events.mapped("event_ticket_ids").unlink()
        events.unlink()
