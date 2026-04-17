"""Postcondition checks for calendar.create_all_day_event_with_attendee."""

from datetime import date
import re

import pytz


def check(env):
    failures = []

    event = env["calendar.event"].search([("name", "=", "Operations Offsite")], limit=1)
    if not event:
        return ["Event 'Operations Offsite' not found"]

    if not event.allday:
        failures.append("Event is not marked as all-day")
    if event.recurrency:
        failures.append("Event should not be recurring")
    if event.location != "Mountain View Campus":
        failures.append(
            f"Location is '{event.location}', expected 'Mountain View Campus'"
        )

    admin = env["res.users"].search([("login", "=", "admin")], limit=1)
    tz_name = (admin.tz if admin else None) or env.user.tz or "UTC"
    try:
        user_tz = pytz.timezone(tz_name)
    except Exception:
        user_tz = pytz.UTC

    if event.start:
        local_dt = pytz.UTC.localize(event.start).astimezone(user_tz)
        if local_dt.date() != date(2026, 6, 18):
            failures.append(f"Event date is {local_dt.date()}, expected 2026-06-18")
    else:
        failures.append("Event has no start date")

    desc_text = re.sub(r"<[^>]+>", "", event.description or "").strip()
    expected_desc = "Annual planning offsite for operations leads."
    if expected_desc not in desc_text:
        failures.append(
            f"Description is '{desc_text}', expected to include exact offsite text"
        )

    attendee_names = event.attendee_ids.mapped("partner_id.name")
    if attendee_names != ["Marc Demo"]:
        failures.append(f"Attendees are {attendee_names}, expected ['Marc Demo']")

    return failures
