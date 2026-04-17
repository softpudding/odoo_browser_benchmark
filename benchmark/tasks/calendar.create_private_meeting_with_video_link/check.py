"""Postcondition checks for calendar.create_private_meeting_with_video_link."""

import re


def check(env):
    failures = []
    event = env["calendar.event"].search([("name", "=", "Private Vendor Sync")], limit=1)
    if not event:
        return ["Event 'Private Vendor Sync' not found"]

    if str(event.start) != "2026-05-27 14:00:00":
        failures.append(f"Event start is {event.start!s}, expected 2026-05-27 14:00:00")
    if str(event.stop) != "2026-05-27 15:00:00":
        failures.append(f"Event stop is {event.stop!s}, expected 2026-05-27 15:00:00")

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
