"""Seed a one-time event for the reschedule-event-update-location-attendee task.

Category 2 (MEDIUM): Edit an existing timed event, adjust start/end times,
change the location, and add an attendee.
"""

from datetime import datetime


EVENT_NAME = "Warehouse Safety Briefing"
DISTRACTOR_NAME = "Warehouse Safety Briefing - East"


def setup(env):
    env["calendar.event"].search([
        ("name", "in", [EVENT_NAME, DISTRACTOR_NAME]),
    ]).unlink()

    admin_partner = env.ref("base.user_admin").partner_id
    marc = env["res.users"].search([("name", "=", "Marc Demo")], limit=1)
    if not marc:
        marc_partner = env["res.partner"].search(
            [("name", "=", "Marc Demo")], limit=1
        )
        if not marc_partner:
            marc_partner = env["res.partner"].create({
                "name": "Marc Demo",
                "email": "marc.demo@company.example.com",
            })
        marc = env["res.users"].create({
            "name": "Marc Demo",
            "login": "marc.demo",
            "partner_id": marc_partner.id,
        })

    env["calendar.event"].create({
        "name": EVENT_NAME,
        "start": datetime(2026, 4, 17, 9, 0, 0),
        "stop": datetime(2026, 4, 17, 10, 0, 0),
        "location": "Room 2",
        "description": "Monthly safety briefing for the warehouse team.",
        "allday": False,
        "recurrency": False,
        "partner_ids": [(6, 0, [admin_partner.id])],
    })
    env["calendar.event"].create({
        "name": DISTRACTOR_NAME,
        "start": datetime(2026, 4, 17, 14, 0, 0),
        "stop": datetime(2026, 4, 17, 15, 0, 0),
        "location": "Room 8",
        "description": "Regional safety check-in.",
        "allday": False,
        "recurrency": False,
        "partner_ids": [(6, 0, [admin_partner.id])],
    })
