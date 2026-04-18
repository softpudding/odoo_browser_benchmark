"""Seed for event.create_event_configure_ticket.

Creates a venue partner 'Riverside Convention Center' so the agent can
select it as the event location. The event itself is NOT created — the
agent creates it from scratch with the configured ticket.
"""


EVENT_NAME = "Spring Tech Conference 2026"
VENUE_NAME = "Riverside Convention Center"


def setup(env):
    # Ensure venue partner exists (used as address_id / Location).
    Partner = env["res.partner"]
    venue = Partner.search([("name", "=", VENUE_NAME)], limit=1)
    if not venue:
        Partner.create({
            "name": VENUE_NAME,
            "is_company": True,
            "street": "101 Riverside Drive",
            "city": "San Diego",
            "zip": "92101",
        })

    # Cleanup any previous run of this event.
    events = env["event.event"].search([("name", "=", EVENT_NAME)])
    if events:
        env["event.event.ticket"].search([("event_id", "in", events.ids)]).unlink()
        events.unlink()
    env.flush_all()
