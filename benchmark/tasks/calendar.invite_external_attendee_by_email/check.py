"""Postcondition checks for calendar.invite_external_attendee_by_email.

Validates:
1. A calendar.event named "Benchmark Strategy Sync" exists.
2. The event is on 2026-05-14 (local admin tz) and is a ~1h non-allday event.
3. The event is not recurring.
4. A res.partner with email "vendor.partner@example.com" exists.
5. That external partner is among the event's attendees.
"""

from datetime import date


EVENT_NAME = "Benchmark Strategy Sync"
EXTERNAL_EMAIL = "vendor.partner@example.com"


def check(env):
    failures = []

    event = env["calendar.event"].search([("name", "=", EVENT_NAME)], limit=1)
    if not event:
        return [f"Event '{EVENT_NAME}' not found"]

    # External partner must exist
    ext_partner = env["res.partner"].search(
        [("email", "=", EXTERNAL_EMAIL)], limit=1
    )
    if not ext_partner:
        failures.append(
            f"External partner with email '{EXTERNAL_EMAIL}' not found"
        )

    # Date check in admin timezone
    import pytz
    admin_user = env["res.users"].search([("login", "=", "admin")], limit=1)
    user_tz_name = (admin_user.tz if admin_user else None) or env.user.tz or "UTC"
    try:
        user_tz = pytz.timezone(user_tz_name)
    except Exception:
        user_tz = pytz.UTC

    if event.start:
        local_dt = pytz.UTC.localize(event.start).astimezone(user_tz)
        if local_dt.date() != date(2026, 5, 14):
            failures.append(
                f"Event date is {local_dt.date()}, expected 2026-05-14"
            )
        if local_dt.hour < 9 or local_dt.hour > 11:
            failures.append(
                f"Local start hour is {local_dt.hour}, expected 10 (10 AM)"
            )
    else:
        failures.append("Event has no start date/time")

    # Duration ~1h
    if event.stop and event.start:
        duration_hours = (event.stop - event.start).total_seconds() / 3600
        if duration_hours < 0.5 or duration_hours > 1.5:
            failures.append(
                f"Duration is {duration_hours:.2f}h, expected ~1h"
            )

    if event.allday:
        failures.append("Event is set as all-day, expected timed event")
    if event.recurrency:
        failures.append("Event is recurring, expected one-time")

    # Attendee partner with external email must be on the event
    attendee_emails = [
        (p.email or "").strip().lower()
        for p in event.attendee_ids.mapped("partner_id")
    ]
    if EXTERNAL_EMAIL.lower() not in attendee_emails:
        failures.append(
            f"Attendee emails on event: {attendee_emails}; "
            f"expected '{EXTERNAL_EMAIL}' to be present"
        )

    return failures
