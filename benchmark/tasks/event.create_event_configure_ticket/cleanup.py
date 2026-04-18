"""Cleanup for event.create_event_configure_ticket."""


EVENT_NAME = "Spring Tech Conference 2026"


def cleanup(env):
    events = env["event.event"].search([("name", "=", EVENT_NAME)])
    events.mapped("event_ticket_ids").unlink()
    events.unlink()
