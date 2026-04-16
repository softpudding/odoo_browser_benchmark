"""Postcondition checks for calendar.create_single_event.

Validates:
1. Event "Q2 Strategy Review" exists
2. Date is May 8, 2026
3. Start time around 14:00, end time around 16:00
4. Location is "Conference Room A"
5. Description contains expected text
6. Marc Demo is an attendee
7. Not an all-day or recurring event
"""

from datetime import date


def check(env):
    failures = []

    event = env["calendar.event"].search(
        [("name", "=", "Q2 Strategy Review")], limit=1
    )
    if not event:
        return ["Event 'Q2 Strategy Review' not found"]

    # Check date
    if event.start:
        event_date = event.start.date()
        expected_date = date(2026, 5, 8)
        if event_date != expected_date:
            failures.append(
                f"Event date is {event_date}, expected {expected_date}"
            )

        # Check approximate start time (14:00 UTC or local)
        start_hour = event.start.hour
        if start_hour < 12 or start_hour > 22:
            failures.append(
                f"Start time hour is {start_hour}, expected around 14 (2 PM)"
            )
    else:
        failures.append("Event has no start date/time")

    # Check duration (should be ~2 hours)
    if event.stop and event.start:
        duration_hours = (event.stop - event.start).total_seconds() / 3600
        if duration_hours < 1.5 or duration_hours > 2.5:
            failures.append(
                f"Duration is {duration_hours:.1f}h, expected ~2h"
            )

    # Check location
    if event.location != "Conference Room A":
        failures.append(
            f"Location is '{event.location}', expected 'Conference Room A'"
        )

    # Check not all-day
    if event.allday:
        failures.append("Event is set as all-day, expected timed event")

    # Check not recurring
    if event.recurrency:
        failures.append("Event is recurring, expected one-time")

    # Check description
    desc = event.description or ""
    import re
    desc_text = re.sub(r"<[^>]+>", "", desc).strip()
    if "Q2" not in desc_text or "objectives" not in desc_text.lower():
        failures.append("Description does not contain expected text about Q2 objectives")

    # Check attendees — Marc Demo should be present
    attendee_names = event.attendee_ids.mapped("partner_id.name")
    if "Marc Demo" not in attendee_names:
        failures.append(
            f"Attendees: {attendee_names}; expected 'Marc Demo' to be present"
        )

    return failures
