"""Cleanup for event.configure_three_ticket_tiers."""

EVENT_NAME = "Summer DevCon 2026"


def cleanup(env):
    event = env["event.event"].search([("name", "=", EVENT_NAME)], limit=1)
    if event:
        event.event_ticket_ids.unlink()
        event.unlink()
