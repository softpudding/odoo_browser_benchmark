"""Seed script for calendar.create_recurring_edit_two_occurrences.

Cleans up any leftover events from prior runs and creates a distractor
recurring event with a similar name to test that the agent targets the
correct event.
"""

from datetime import datetime


TITLE = "Cross-Team Sync"
DISTRACTOR_TITLE = "Cross-Team Review"


def _ensure_marc_demo(env):
    """Make sure Marc Demo partner exists for the attendee step."""
    partner = env["res.partner"].search([("name", "=", "Marc Demo")], limit=1)
    if partner:
        return partner
    return env["res.partner"].create({
        "name": "Marc Demo",
        "email": "mark.brown23@example.com",
    })


def setup(env):
    # Set admin timezone to UTC for predictable date handling
    admin = env["res.users"].search([("login", "=", "admin")], limit=1)
    if admin:
        admin.write({"tz": "UTC"})

    # Clean up prior runs
    for title in (TITLE, DISTRACTOR_TITLE):
        old_events = env["calendar.event"].search([("name", "=", title)])
        old_recurrences = old_events.mapped("recurrence_id")
        old_events.with_context(dont_notify=True).unlink()
        old_recurrences.unlink()

    # Ensure Marc Demo partner is available
    _ensure_marc_demo(env)

    # Create a distractor recurring event with a similar name
    admin_partner = admin.partner_id
    env["calendar.event"].create({
        "name": DISTRACTOR_TITLE,
        "start": datetime(2026, 6, 5, 14, 0),
        "stop": datetime(2026, 6, 5, 15, 0),
        "location": "Room 101",
        "partner_ids": [(4, admin_partner.id)],
        "recurrency": True,
        "rrule_type": "weekly",
        "fri": True,
        "interval": 1,
        "end_type": "count",
        "count": 4,
    })
