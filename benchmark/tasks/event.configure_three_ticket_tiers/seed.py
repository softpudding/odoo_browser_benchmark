"""Seed for event.configure_three_ticket_tiers.

Creates event 'Summer DevCon 2026' with NO tickets initially; task adds
three tiers.
"""

EVENT_NAME = "Summer DevCon 2026"


def setup(env):
    # Clean prior tickets for any previous run of this event.
    event = env["event.event"].search([("name", "=", EVENT_NAME)], limit=1)
    if event:
        event.event_ticket_ids.unlink()
    values = {
        "name": EVENT_NAME,
        "date_begin": "2026-08-12 09:00:00",
        "date_end": "2026-08-14 17:00:00",
    }
    if not event:
        event = env["event.event"].create(values)
    else:
        event.write(values)

    # Odoo auto-creates a default registration ticket when a new event
    # is saved (via compute/default). Flush first, then remove ALL
    # tickets on this event — searching directly in case the o2m cache
    # is stale.
    env.flush_all()
    env["event.event.ticket"].search([("event_id", "=", event.id)]).unlink()
    env.flush_all()
