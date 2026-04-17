"""Seed for event.create_event_add_ticket.

Category 2 (MEDIUM): Create an event with a paid ticket type.
The agent must fill in event name, add a ticket line with name, price,
and seat limit.
We pre-create the event with dates to avoid daterange widget issues,
but leave name empty and no tickets — the agent must complete it.
"""

EVENT_NAME = "Odoo Community Days 2026"


def setup(env):
    # Cleanup prior runs
    old_events = env["event.event"].search([
        ("name", "=", EVENT_NAME),
    ])
    if old_events:
        env["event.registration"].search([
            ("event_id", "in", old_events.ids),
        ]).unlink()
        old_events.unlink()

    # Also clean up any draft events with empty names from prior failed runs
    draft_events = env["event.event"].search([
        ("name", "in", [False, "", "New"]),
    ])
    if draft_events:
        env["event.registration"].search([
            ("event_id", "in", draft_events.ids),
        ]).unlink()
        draft_events.unlink()
