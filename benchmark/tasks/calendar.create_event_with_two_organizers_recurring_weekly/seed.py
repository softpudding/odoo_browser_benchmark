"""Seed for calendar.create_event_with_two_organizers_recurring_weekly.

Ensures admin's partner is named "Alice Admin" and a standalone
"Bob Test" partner exists. Cleans up any leftover "Weekly Standup"
event from prior runs.
"""


EVENT_NAME = "Weekly Standup"


def setup(env):
    # Set admin timezone to UTC for predictable datetime handling
    admin = env["res.users"].search([("login", "=", "admin")], limit=1)
    if admin:
        admin.write({"tz": "UTC"})
        # Rename admin's partner to "Alice Admin" so the agent has a
        # specific organizer name to add as an attendee.
        admin.partner_id.write({"name": "Alice Admin"})

    # Ensure Bob Test partner exists
    bob = env["res.partner"].search([("name", "=", "Bob Test")], limit=1)
    if not bob:
        env["res.partner"].create({
            "name": "Bob Test",
            "email": "bob.test@example.com",
        })

    # Clean up prior run artifacts
    old = env["calendar.event"].search([("name", "=", EVENT_NAME)])
    old_recurrences = old.mapped("recurrence_id")
    old.with_context(dont_notify=True).unlink()
    old_recurrences.unlink()
