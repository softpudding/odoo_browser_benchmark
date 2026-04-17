"""Cleanup-only seed for an event creation task."""


EVENT_NAME = "Operations Leadership Summit 2026"


def setup(env):
    events = env["event.event"].search([("name", "=", EVENT_NAME)])
    events.mapped("event_ticket_ids").unlink()
    events.unlink()
