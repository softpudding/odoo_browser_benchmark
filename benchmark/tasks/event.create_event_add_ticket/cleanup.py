"""Clean up artifacts from previous runs."""

EVENT_NAME = "Odoo Community Days 2026"


def cleanup(env):
    events = env["event.event"].search([("name", "=", EVENT_NAME)])
    if events:
        env["event.registration"].search([
            ("event_id", "in", events.ids),
        ]).unlink()
        events.unlink()
