"""Seed a recurring weekly event for a single-occurrence all-day edit.

Category 5: Deep UI interaction.
The agent must change one occurrence to all-day and use the
recurrence dialog correctly so the rest of the series stays timed.
"""

from datetime import datetime


def setup(env):
    admin = env.ref("base.user_admin")
    partner = admin.partner_id

    events = env["calendar.event"].search([("name", "=", "Warehouse Walkthrough")])
    recurrences = events.mapped("recurrence_id")
    events.with_context(dont_notify=True).unlink()
    recurrences.unlink()

    env["calendar.event"].create({
        "name": "Warehouse Walkthrough",
        "start": datetime(2026, 5, 5, 14, 0),
        "stop": datetime(2026, 5, 5, 15, 0),
        "location": "North Annex",
        "partner_ids": [(4, partner.id)],
        "recurrency": True,
        "rrule_type": "weekly",
        "tue": True,
        "interval": 1,
        "end_type": "count",
        "count": 4,
    })
