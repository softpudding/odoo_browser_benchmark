"""Postcondition checks for calendar.create_event_with_two_organizers_recurring_weekly.

Validates that:
- One non-all-day calendar.event named "Weekly Standup" exists.
- Start/stop are 2026-06-01 09:00 and 09:30.
- Recurrence is weekly on Monday with interval 1, end_date 2026-12-31.
- Both Alice Admin and Bob Test are attendees.
- A built-in Discuss videocall URL is set on the event.
"""

from datetime import date


EVENT_NAME = "Weekly Standup"


def check(env):
    failures = []
    events = env["calendar.event"].search([("name", "=", EVENT_NAME)])
    # The base event is the one starting on 2026-06-01.
    base = events.filtered(lambda e: e.start and e.start.date() == date(2026, 6, 1))
    if not base:
        return [f"No '{EVENT_NAME}' event found starting on 2026-06-01"]
    if len(base) > 1:
        failures.append(f"Found {len(base)} base events on 2026-06-01, expected 1")
    base = base[0]

    # ── Datetime checks ──────────────────────────────────────────────
    if str(base.start) != "2026-06-01 09:00:00":
        failures.append(f"Start is {base.start!s}, expected 2026-06-01 09:00:00")
    if str(base.stop) != "2026-06-01 09:30:00":
        failures.append(f"Stop is {base.stop!s}, expected 2026-06-01 09:30:00")
    if base.allday:
        failures.append("Event is all-day, expected timed event")

    # ── Recurrence checks ────────────────────────────────────────────
    if not base.recurrency:
        failures.append("Base event is not marked as recurring")
    if not base.recurrence_id:
        failures.append("Base event has no recurrence_id")
    else:
        rec = base.recurrence_id
        if rec.rrule_type != "weekly":
            failures.append(f"rrule_type is {rec.rrule_type!r}, expected 'weekly'")
        if int(rec.interval or 0) != 1:
            failures.append(f"interval is {rec.interval!r}, expected 1")
        if not rec.mon:
            failures.append("Recurrence does not include Monday (mon=False)")
        # Other weekdays should be False
        for day_attr, day_label in [
            ("tue", "Tuesday"), ("wed", "Wednesday"), ("thu", "Thursday"),
            ("fri", "Friday"), ("sat", "Saturday"), ("sun", "Sunday"),
        ]:
            if getattr(rec, day_attr):
                failures.append(f"Recurrence unexpectedly includes {day_label}")
        if rec.end_type != "end_date":
            failures.append(f"end_type is {rec.end_type!r}, expected 'end_date'")
        if rec.until != date(2026, 12, 31):
            failures.append(f"until is {rec.until!r}, expected 2026-12-31")

    # ── Attendees ────────────────────────────────────────────────────
    attendee_names = set(base.partner_ids.mapped("name"))
    if "Alice Admin" not in attendee_names:
        failures.append(f"Alice Admin not in attendees: {sorted(attendee_names)}")
    if "Bob Test" not in attendee_names:
        failures.append(f"Bob Test not in attendees: {sorted(attendee_names)}")

    # ── Videocall URL ────────────────────────────────────────────────
    vcl = base.videocall_location or ""
    if "/calendar/join_videocall/" not in vcl:
        failures.append(
            f"videocall_location is {vcl!r}, expected built-in /calendar/join_videocall/ URL"
        )

    return failures
