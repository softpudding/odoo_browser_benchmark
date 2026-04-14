"""Seed a recurring weekly calendar event with 4 occurrences.

Category 5: Deep UI interaction.
The agent must edit only one occurrence of a recurring event,
handling the recurrence_update dialog correctly ("This Event" only).
Browser-use typically fails on the recurrence radio-button dialog.
"""

from datetime import datetime


def setup(env):
    admin = env.ref("base.user_admin")
    partner = admin.partner_id

    # Cleanup prior runs — remove events and recurrences
    old_events = env["calendar.event"].search([("name", "=", "Ops Standup")])
    old_recurrences = old_events.mapped("recurrence_id")
    old_events.with_context(dont_notify=True).unlink()
    old_recurrences.unlink()

    # Create a recurring weekly event: every Monday, 4 occurrences
    # Starting Monday April 13, 2026 at 09:00 UTC
    env["calendar.event"].create({
        "name": "Ops Standup",
        "start": datetime(2026, 4, 13, 9, 0),
        "stop": datetime(2026, 4, 13, 10, 0),
        "location": "Main Office",
        "partner_ids": [(4, partner.id)],
        "recurrency": True,
        "rrule_type": "weekly",
        "mon": True,
        "interval": 1,
        "end_type": "count",
        "count": 4,
    })
