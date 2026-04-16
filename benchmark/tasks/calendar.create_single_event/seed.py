"""Seed for the create-single-event task.

Category 2 (MEDIUM): Create a one-time calendar event with multiple
fields: title, date, start/end time, location, description, and attendee.
The date/time picker and attendee selection can be tricky for browser agents.
"""

EVENT_NAME = "Q2 Strategy Review"


def setup(env):
    # --- Cleanup prior runs ---
    old_events = env["calendar.event"].search([("name", "=", EVENT_NAME)])
    old_events.unlink()

    # --- Ensure Marc Demo user exists ---
    marc = env["res.users"].search([("name", "=", "Marc Demo")], limit=1)
    if not marc:
        marc_partner = env["res.partner"].search(
            [("name", "=", "Marc Demo")], limit=1
        )
        if not marc_partner:
            marc_partner = env["res.partner"].create({
                "name": "Marc Demo",
                "email": "marc.demo@company.com",
            })
        marc = env["res.users"].create({
            "name": "Marc Demo",
            "login": "marc.demo",
            "partner_id": marc_partner.id,
        })
