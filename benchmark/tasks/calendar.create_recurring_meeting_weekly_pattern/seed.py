"""Seed for calendar.create_recurring_meeting_weekly_pattern.

Difficulty: medium (Category: deep_ui_interaction).

The agent must:
  - Create a calendar.event 'Bench Weekly Standup' on 2026-05-04 10:00-10:30
    (a Monday) in UTC (admin tz forced to UTC for deterministic datetime).
  - Toggle Recurrence ON, set weekly on Monday only, and configure the
    count-based end type (count=4 — i.e. exactly 4 occurrences).
  - Save the event.

Seed responsibilities:
  - Force admin.tz='UTC' so typed datetimes are stored as-is in UTC.
  - Wipe any leftover 'Bench Weekly Standup' events (and their calendar.recurrence
    parents) from prior runs so the check counts are deterministic.
  - Do NOT pre-create the event; the agent creates it.
"""


EVENT_NAME = "Bench Weekly Standup"


def setup(env):
    # Admin tz=UTC so typed UI times map 1:1 to stored UTC datetimes.
    admin = env["res.users"].search([("login", "=", "admin")], limit=1)
    if admin and admin.tz != "UTC":
        admin.write({"tz": "UTC"})

    # Cleanup any leftover event(s) from prior runs. Include archived via
    # active_test=False in case a prior run left inactive base events.
    events = env["calendar.event"].with_context(active_test=False).search([
        ("name", "=", EVENT_NAME),
    ])
    if events:
        recurrences = events.mapped("recurrence_id")
        attachments = env["ir.attachment"].search([
            ("res_model", "=", "calendar.event"),
            ("res_id", "in", events.ids),
        ])
        if attachments:
            attachments.unlink()
        events.with_context(dont_notify=True).unlink()
        if recurrences:
            recurrences.unlink()
