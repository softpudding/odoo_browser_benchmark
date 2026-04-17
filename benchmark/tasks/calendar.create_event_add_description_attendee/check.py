"""Postcondition checks for calendar.create_event_add_description_attendee."""

from datetime import date
import pytz
import re


def check(env):
    failures = []
    event = env["calendar.event"].search([("name", "=", "Vendor Kickoff Briefing")], limit=1)
    if not event:
        return ["Event 'Vendor Kickoff Briefing' not found"]

    admin_user = env["res.users"].search([("login", "=", "admin")], limit=1)
    user_tz_name = (admin_user.tz if admin_user else None) or env.user.tz or "UTC"
    try:
        user_tz = pytz.timezone(user_tz_name)
    except Exception:
        user_tz = pytz.UTC

    if event.start:
        local_dt = pytz.UTC.localize(event.start).astimezone(user_tz)
        if local_dt.date() != date(2026, 5, 22):
            failures.append(f"Event date is {local_dt.date()}, expected 2026-05-22")
        if local_dt.hour < 10 or local_dt.hour > 12:
            failures.append(f"Local start hour is {local_dt.hour}, expected 11")
    else:
        failures.append("Event has no start date/time")

    if event.stop and event.start:
        duration_hours = (event.stop - event.start).total_seconds() / 3600
        if duration_hours < 1.4 or duration_hours > 1.6:
            failures.append(f"Duration is {duration_hours:.1f}h, expected 1.5h")

    if event.location != "Room 204":
        failures.append(f"Location is '{event.location}', expected 'Room 204'")
    if event.allday:
        failures.append("Event is set as all-day, expected timed event")
    if event.recurrency:
        failures.append("Event is recurring, expected one-time")

    desc_text = re.sub(r"<[^>]+>", "", event.description or "").strip().lower()
    if "kickoff" not in desc_text or "owners" not in desc_text:
        failures.append("Description does not contain expected text about kickoff owners")

    attendee_names = event.attendee_ids.mapped("partner_id.name")
    if "Marc Demo" not in attendee_names:
        failures.append(f"Attendees: {attendee_names}; expected 'Marc Demo'")
    return failures
