"""Cleanup for event.create_event_add_ticket."""


def cleanup(env):
    events = env["event.event"].search([("name", "=", "Operations Leadership Summit 2026")])
    events.mapped("event_ticket_ids").unlink()
    events.unlink()
