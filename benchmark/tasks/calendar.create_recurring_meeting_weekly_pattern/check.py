"""Postcondition checks for calendar.create_recurring_meeting_weekly_pattern.

Validates:
- A base calendar.event 'Bench Weekly Standup' exists with first occurrence
  falling on Monday (target week-of 2026-05-04) in the admin user's local tz.
- Base event has a 30-minute duration and is NOT all-day.
- Base event recurrency=True and has a calendar.recurrence parent.
- Recurrence rrule contains FREQ=WEEKLY, COUNT=4, BYDAY=MO.
- Recurrence expands to exactly 4 calendar.event rows on 4 consecutive Mondays.
- Exactly 4 events total with the given name.

The absolute time-of-day is intentionally not checked: the Odoo web datetime
widget interprets typed strings in the browser's local tz, which diverges
from the admin user's tz on some harnesses. The task still nails down the
"weekly on Monday × 4" recurrence pattern, which is what the prompt asks.
"""

from datetime import date, timedelta

import pytz


EVENT_NAME = "Bench Weekly Standup"
EXPECTED_FIRST_MONDAY = date(2026, 5, 4)
EXPECTED_DURATION_MINUTES = 30


def _admin_tz(env):
    admin = env["res.users"].search([("login", "=", "admin")], limit=1)
    tz_name = (admin.tz if admin else None) or env.user.tz or "UTC"
    try:
        return pytz.timezone(tz_name)
    except Exception:
        return pytz.UTC


def check(env):
    failures = []

    events = env["calendar.event"].with_context(active_test=False).search([
        ("name", "=", EVENT_NAME),
    ])
    if not events:
        return [f"No calendar.event named {EVENT_NAME!r} found"]

    # ── Base event: the first occurrence whose admin-local date is 2026-05-04
    admin_tz = _admin_tz(env)

    def _local_date(e):
        if not e.start:
            return None
        return pytz.UTC.localize(e.start).astimezone(admin_tz).date()

    base = events.filtered(lambda e: _local_date(e) == EXPECTED_FIRST_MONDAY)
    if not base:
        observed = sorted(str(e.start) for e in events)
        return [
            f"No {EVENT_NAME!r} occurrence whose admin-local date is "
            f"{EXPECTED_FIRST_MONDAY}; stored starts: {observed!r}"
        ]
    if len(base) > 1:
        failures.append(f"Found {len(base)} base events on {EXPECTED_FIRST_MONDAY}, expected 1")
    base = base[0]

    # Duration must be 30 min (independent of tz).
    if base.start and base.stop:
        duration_minutes = int((base.stop - base.start).total_seconds() / 60)
        if duration_minutes != EXPECTED_DURATION_MINUTES:
            failures.append(
                f"Duration is {duration_minutes} minutes, expected {EXPECTED_DURATION_MINUTES}"
            )
    else:
        failures.append("Base event missing start or stop datetime")

    if base.allday:
        failures.append("Base event is marked all-day; expected timed event")

    # ── Recurrence flags ─────────────────────────────────────────────
    if not base.recurrency:
        failures.append("Base event recurrency flag is False; expected True")
    if not base.recurrence_id:
        failures.append("Base event has no recurrence_id; expected calendar.recurrence link")

    rec = base.recurrence_id
    if rec:
        # rrule_type (stored selection) + rrule (computed RRULE string).
        if rec.rrule_type != "weekly":
            failures.append(f"rrule_type is {rec.rrule_type!r}, expected 'weekly'")
        if int(rec.interval or 0) != 1:
            failures.append(f"interval is {rec.interval!r}, expected 1")
        if rec.end_type != "count":
            failures.append(f"end_type is {rec.end_type!r}, expected 'count'")
        if int(rec.count or 0) != 4:
            failures.append(f"count is {rec.count!r}, expected 4")
        if not rec.mon:
            failures.append("Recurrence does not include Monday (mon=False)")
        for day_attr, day_label in [
            ("tue", "Tuesday"), ("wed", "Wednesday"), ("thu", "Thursday"),
            ("fri", "Friday"), ("sat", "Saturday"), ("sun", "Sunday"),
        ]:
            if getattr(rec, day_attr):
                failures.append(f"Recurrence unexpectedly includes {day_label}")

        rrule = rec.rrule or ""
        if "FREQ=WEEKLY" not in rrule:
            failures.append(f"rrule {rrule!r} missing FREQ=WEEKLY")
        if "COUNT=4" not in rrule:
            failures.append(f"rrule {rrule!r} missing COUNT=4")
        if "BYDAY=MO" not in rrule:
            failures.append(f"rrule {rrule!r} missing BYDAY=MO")

        # Expanded occurrences count: weekly count=4 → exactly 4 events.
        expanded = env["calendar.event"].with_context(active_test=False).search([
            ("recurrence_id", "=", rec.id),
            ("name", "=", EVENT_NAME),
        ])
        if len(expanded) != 4:
            failures.append(
                f"Recurrence expanded to {len(expanded)} event(s), expected 4; "
                f"starts: {sorted(str(e.start) for e in expanded)!r}"
            )
        # Every expanded occurrence should land on a Monday in admin-local tz,
        # and the four local dates should be 5/4, 5/11, 5/18, 5/25.
        local_dates = sorted(
            pytz.UTC.localize(e.start).astimezone(admin_tz).date()
            for e in expanded
            if e.start
        )
        expected_dates = [EXPECTED_FIRST_MONDAY + timedelta(weeks=i) for i in range(4)]
        if local_dates != expected_dates:
            failures.append(
                f"Expanded local dates are {local_dates!r}, expected {expected_dates!r}"
            )

    # There must be exactly one event named 'Bench Weekly Standup' per recurrence
    # occurrence — so total count is 4 overall.
    if len(events) != 4:
        failures.append(
            f"Expected 4 calendar.event rows named {EVENT_NAME!r}, got {len(events)}; "
            f"starts: {sorted(str(e.start) for e in events)!r}"
        )

    return failures
