"""Postcondition checks for calendar.configure_meeting_with_location_and_reminder."""

from datetime import date
import pytz


EVENT_NAME = "Quarterly Review"
EXPECTED_LOCATION = "Conference Room B, Floor 3"
REQUIRED_ATTENDEES = {"Alice Attendee", "Bob Attendee"}
EXPECTED_DATE = date(2026, 6, 10)
EXPECTED_LOCAL_START_HOUR = 14  # 2 PM
EXPECTED_DURATION_HOURS = 2.0
EXPECTED_ALARM_MINUTES = 60


def check(env):
    failures = []

    events = env["calendar.event"].search([("name", "=", EVENT_NAME)])
    if len(events) == 0:
        return [f"Event {EVENT_NAME!r} not found"]
    if len(events) > 1:
        failures.append(
            f"Expected exactly 1 event named {EVENT_NAME!r}, found {len(events)}"
        )
    event = events[0]

    # Flags / recurrence / allday.
    if event.allday:
        failures.append("Event is marked all-day; expected a timed event")
    if event.recurrency:
        failures.append("Event is recurring; expected a one-time event")

    # Location.
    if (event.location or "") != EXPECTED_LOCATION:
        failures.append(
            f"Event location is {event.location!r}, "
            f"expected {EXPECTED_LOCATION!r}"
        )

    # Date + time (admin tz).
    admin_user = env["res.users"].search([("login", "=", "admin")], limit=1)
    tz_name = (admin_user.tz if admin_user else None) or env.user.tz or "UTC"
    try:
        user_tz = pytz.timezone(tz_name)
    except Exception:
        user_tz = pytz.UTC

    if not event.start:
        failures.append("Event has no start datetime")
    else:
        local_start = pytz.UTC.localize(event.start).astimezone(user_tz)
        if local_start.date() != EXPECTED_DATE:
            failures.append(
                f"Event local start date is {local_start.date()}, "
                f"expected {EXPECTED_DATE}"
            )
        # Accept ±1h to tolerate timezone drift between seed + runtime tz.
        if abs(local_start.hour - EXPECTED_LOCAL_START_HOUR) > 1:
            failures.append(
                f"Event local start hour is {local_start.hour}, "
                f"expected {EXPECTED_LOCAL_START_HOUR} (2 PM)"
            )
        if local_start.minute != 0:
            failures.append(
                f"Event start minute is {local_start.minute}, expected 00"
            )

    if event.start and event.stop:
        duration = (event.stop - event.start).total_seconds() / 3600.0
        if abs(duration - EXPECTED_DURATION_HOURS) > 0.1:
            failures.append(
                f"Event duration is {duration:.2f}h, expected 2.0h"
            )

    # Attendees: the two required users must be present (organizer may also be).
    partner_names = set(event.partner_ids.mapped("name"))
    missing_partners = REQUIRED_ATTENDEES - partner_names
    if missing_partners:
        failures.append(
            f"Missing required partner_ids: {sorted(missing_partners)!r}; "
            f"present: {sorted(partner_names)!r}"
        )
    attendee_names = set(event.attendee_ids.mapped("partner_id.name"))
    missing_attendees = REQUIRED_ATTENDEES - attendee_names
    if missing_attendees:
        failures.append(
            f"Missing required attendees: {sorted(missing_attendees)!r}; "
            f"present: {sorted(attendee_names)!r}"
        )

    # Reminder: at least one calendar.alarm linked with duration_minutes == 60.
    alarms = event.alarm_ids
    if not alarms:
        failures.append("Event has no alarms/reminders; expected one 1h reminder")
    else:
        matching = alarms.filtered(lambda a: a.duration_minutes == EXPECTED_ALARM_MINUTES)
        if not matching:
            failures.append(
                f"No alarm with duration_minutes=={EXPECTED_ALARM_MINUTES} on event; "
                f"alarms: {[(a.name, a.duration_minutes) for a in alarms]!r}"
            )
        if len(alarms) > 1:
            failures.append(
                f"Expected exactly 1 alarm on event, found {len(alarms)}: "
                f"{[(a.name, a.duration_minutes) for a in alarms]!r}"
            )

    return failures
