"""Seed for calendar.configure_meeting_with_location_and_reminder.

Difficulty: medium (Category: deep_ui_interaction).
The agent must:
  - Create a calendar.event 'Quarterly Review' on 2026-06-10 14:00-16:00 local.
  - Set `location` to 'Conference Room B, Floor 3'.
  - Add two seeded internal users (Alice Attendee + Bob Attendee) as attendees.
  - Open the Options tab and add a 1-hour-before reminder to `alarm_ids`
    (the pre-existing `Notification - 1 Hours` calendar.alarm satisfies this).
  - Save the event.

Seed responsibilities:
  - Wipe any prior 'Quarterly Review' events (and attachments/invitation.ics).
  - Ensure internal users 'Alice Attendee' and 'Bob Attendee' exist as
    res.users with matching res.partner, so the agent can add them via
    autocomplete.
  - Do NOT pre-create the event; the agent creates it.
"""

EVENT_NAME = "Quarterly Review"
ATTENDEE_USERS = (
    {"name": "Alice Attendee", "login": "alice.attendee", "email": "alice.attendee@example.com"},
    {"name": "Bob Attendee", "login": "bob.attendee", "email": "bob.attendee@example.com"},
)


def setup(env):
    # Cleanup any leftover event(s) from previous runs (and their
    # auto-created invitation.ics attachments so cleanup is fully idempotent).
    events = env["calendar.event"].with_context(active_test=False).search([
        ("name", "=", EVENT_NAME),
    ])
    if events:
        attachments = env["ir.attachment"].search([
            ("res_model", "=", "calendar.event"),
            ("res_id", "in", events.ids),
        ])
        if attachments:
            attachments.unlink()
        events.unlink()

    # Ensure the two attendee users exist. Create res.partner + res.users.
    for spec in ATTENDEE_USERS:
        user = env["res.users"].with_context(active_test=False).search(
            [("login", "=", spec["login"])], limit=1,
        )
        if user:
            if not user.active:
                user.active = True
            # Keep name / email in sync.
            if user.name != spec["name"]:
                user.name = spec["name"]
            if user.partner_id and user.partner_id.email != spec["email"]:
                user.partner_id.email = spec["email"]
            continue
        partner = env["res.partner"].search(
            [("name", "=", spec["name"])], limit=1,
        )
        if not partner:
            partner = env["res.partner"].create({
                "name": spec["name"],
                "email": spec["email"],
            })
        else:
            if partner.email != spec["email"]:
                partner.email = spec["email"]
        env["res.users"].create({
            "name": spec["name"],
            "login": spec["login"],
            "email": spec["email"],
            "partner_id": partner.id,
        })
