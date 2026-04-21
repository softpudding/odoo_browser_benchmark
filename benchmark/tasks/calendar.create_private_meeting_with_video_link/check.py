"""Postcondition checks for calendar.create_private_meeting_with_video_link."""

import re
from datetime import date


def check(env):
    failures = []
    event = env["calendar.event"].search([("name", "=", "Private Vendor Sync")], limit=1)
    if not event:
        return ["Event 'Private Vendor Sync' not found"]

    # Convert stored UTC to admin-local time for comparison.
    import pytz
    admin_user = env["res.users"].search([("login", "=", "admin")], limit=1)
    user_tz_name = (admin_user.tz if admin_user else None) or env.user.tz or "UTC"
    try:
        user_tz = pytz.timezone(user_tz_name)
    except Exception:
        user_tz = pytz.UTC

    if event.start:
        local_start = pytz.UTC.localize(event.start).astimezone(user_tz)
        expected_date = date(2026, 5, 27)
        if local_start.date() != expected_date:
            failures.append(f"Event date is {local_start.date()}, expected {expected_date}")
        if local_start.hour != 14 or local_start.minute != 0:
            failures.append(f"Local start time is {local_start.strftime('%H:%M')}, expected 14:00")
    else:
        failures.append("Event has no start date/time")

    if event.stop and event.start:
        duration_hours = (event.stop - event.start).total_seconds() / 3600
        if duration_hours < 0.5 or duration_hours > 1.5:
            failures.append(f"Duration is {duration_hours:.1f}h, expected ~1h")

    if event.location != "Bridge Room":
        failures.append(f"Location is '{event.location}', expected 'Bridge Room'")
    if event.allday:
        failures.append("Event is set as all-day, expected timed event")
    if event.recurrency:
        failures.append("Event is recurring, expected one-time")
    if event.privacy != "private":
        failures.append(f"Privacy is {event.privacy!r}, expected 'private'")
    if not event.videocall_location or "/calendar/join_videocall/" not in event.videocall_location:
        failures.append("Event does not have the expected built-in videocall URL")

    desc_text = re.sub(r"<[^>]+>", "", event.description or "").strip().lower()
    if "blocker owners" not in desc_text or "supplier handoff plan" not in desc_text:
        failures.append("Description does not contain the expected blocker and handoff text")

    attendee_names = event.attendee_ids.mapped("partner_id.name")
    if "Marc Demo" not in attendee_names:
        failures.append(f"Attendees: {attendee_names}; expected 'Marc Demo'")
    return failures
