"""Postcondition checks for calendar.invite_organize_with_event_agenda_attachment."""

from datetime import date
import pytz


EVENT_NAME = "Q2 Planning Session"
REQUIRED_ATTENDEES = {"Alice Bench", "Bob Bench"}
EXPECTED_ATTACHMENT_NAME = "agenda.txt"
EXPECTED_DATE = date(2026, 5, 20)
EXPECTED_LOCAL_START_HOUR = 14  # 2 PM
EXPECTED_DURATION_HOURS = 1.5


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
        # Also pin the minute to 00 (prompt says 2:00, 3:30).
        if local_start.minute != 0:
            failures.append(
                f"Event start minute is {local_start.minute}, expected 00"
            )

    if event.start and event.stop:
        duration = (event.stop - event.start).total_seconds() / 3600.0
        if abs(duration - EXPECTED_DURATION_HOURS) > 0.1:
            failures.append(
                f"Event duration is {duration:.2f}h, expected 1.5h"
            )

    # Attendees: exactly the two expected partners must be present.
    attendee_names = set(event.attendee_ids.mapped("partner_id.name"))
    missing = REQUIRED_ATTENDEES - attendee_names
    if missing:
        failures.append(
            f"Missing required attendees: {sorted(missing)!r}; "
            f"present: {sorted(attendee_names)!r}"
        )

    # Partner_ids also used by some pipelines; sanity-check that the two
    # required partners are on the event.
    partner_names = set(event.partner_ids.mapped("name"))
    missing_partners = REQUIRED_ATTENDEES - partner_names
    if missing_partners:
        failures.append(
            f"Missing required partner_ids: {sorted(missing_partners)!r}; "
            f"present: {sorted(partner_names)!r}"
        )

    # Attachment: exactly 1 agenda.txt linked to this event.
    attachments = env["ir.attachment"].search([
        ("res_model", "=", "calendar.event"),
        ("res_id", "=", event.id),
    ])
    agenda_attachments = attachments.filtered(
        lambda a: (a.name or "").lower() == EXPECTED_ATTACHMENT_NAME
    )
    if len(agenda_attachments) == 0:
        failures.append(
            f"No ir.attachment named {EXPECTED_ATTACHMENT_NAME!r} linked to "
            f"calendar event id={event.id}; all attachments: "
            f"{attachments.mapped('name')!r}"
        )
    elif len(agenda_attachments) > 1:
        failures.append(
            f"Expected exactly 1 {EXPECTED_ATTACHMENT_NAME!r} attachment, "
            f"found {len(agenda_attachments)}"
        )
    else:
        att = agenda_attachments[0]
        if not att.datas and not att.raw:
            failures.append(
                f"Attachment {EXPECTED_ATTACHMENT_NAME!r} has empty content"
            )

    return failures
