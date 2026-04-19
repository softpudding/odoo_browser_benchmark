"""Postcondition checks for hr.create_public_holiday_calendar_entry.

Validates:
- Exactly one resource.calendar.leaves row named 'Bench Founder Day'
  exists.
- That row is company-wide: resource_id is False.
- date_from / date_to COVER the target calendar day 2026-06-01 — i.e.
  the holiday span must overlap with at least some portion of
  2026-06-01 in the admin user's timezone. We don't pin the exact
  stored UTC timestamps because the Odoo web datetime widget interprets
  typed strings in the browser's local tz and the benchmark harness's
  browser tz may diverge from the admin's Odoo tz by several hours;
  either way the typed 06/01/2026 00:00 -> 23:59 must cover the target
  calendar day in at least one of UTC, admin-local, or browser-local tz.
- date_to >= date_from and the span is at least 1 hour (avoid a
  zero-length / accidental identical-datetime save).
"""

from datetime import date, datetime, timedelta

import pytz


HOLIDAY_NAME = "Bench Founder Day"
EXPECTED_DATE = date(2026, 6, 1)
# Tzs a typical benchmark harness browser might use. If the stored span
# overlaps 2026-06-01 in any of these, we accept it: the agent clearly
# intended the right calendar day, just routed through the widget's tz
# coercion. Admin's actual tz (set to UTC in seed) is tried first.
_CANDIDATE_TZS = [
    "UTC",
    "America/Los_Angeles",
    "America/New_York",
    "Europe/Paris",
    "Asia/Shanghai",
    "Asia/Singapore",
]


def _admin_tz(env):
    admin = env["res.users"].search([("login", "=", "admin")], limit=1)
    tz_name = (admin.tz if admin else None) or env.user.tz or "UTC"
    try:
        return pytz.timezone(tz_name)
    except Exception:
        return pytz.UTC


def _covers_target_in_tz(date_from_utc, date_to_utc, target, tz_name):
    """Return True if [date_from_utc, date_to_utc] overlaps the
    calendar day `target` when interpreted in the given tz.
    """
    try:
        tz = pytz.timezone(tz_name)
    except Exception:
        return False
    day_start = tz.localize(datetime.combine(target, datetime.min.time()))
    day_end = tz.localize(datetime.combine(target, datetime.max.time()))
    day_start_utc = day_start.astimezone(pytz.UTC).replace(tzinfo=None)
    day_end_utc = day_end.astimezone(pytz.UTC).replace(tzinfo=None)
    # Overlap: max(start) <= min(end)
    return max(date_from_utc, day_start_utc) <= min(date_to_utc, day_end_utc)


def check(env):
    failures = []

    rows = env["resource.calendar.leaves"].search(
        [("name", "=", HOLIDAY_NAME)]
    )
    if not rows:
        return [f"No resource.calendar.leaves row named {HOLIDAY_NAME!r} found"]
    if len(rows) > 1:
        failures.append(
            f"Expected exactly 1 {HOLIDAY_NAME!r} row, found {len(rows)}"
        )

    holiday = rows[0]

    if holiday.resource_id:
        failures.append(
            f"{HOLIDAY_NAME!r} has resource_id={holiday.resource_id.name!r}; "
            f"expected False (company-wide public holiday)"
        )

    if not holiday.date_from:
        failures.append(f"{HOLIDAY_NAME!r} has no date_from")
    if not holiday.date_to:
        failures.append(f"{HOLIDAY_NAME!r} has no date_to")

    if holiday.date_from and holiday.date_to:
        if holiday.date_from > holiday.date_to:
            failures.append(
                f"{HOLIDAY_NAME!r} date_from {holiday.date_from} is after "
                f"date_to {holiday.date_to}"
            )
        else:
            span = holiday.date_to - holiday.date_from
            if span < timedelta(minutes=60):
                failures.append(
                    f"{HOLIDAY_NAME!r} spans {span} "
                    f"({holiday.date_from} -> {holiday.date_to}); "
                    f"expected a full-day holiday (~24h)"
                )

        # Must cover 2026-06-01 in at least one plausible tz. We also
        # always include the admin's current tz.
        candidates = list(_CANDIDATE_TZS)
        admin_tz_name = _admin_tz(env).zone
        if admin_tz_name not in candidates:
            candidates.append(admin_tz_name)
        covers = any(
            _covers_target_in_tz(
                holiday.date_from, holiday.date_to, EXPECTED_DATE, tz
            )
            for tz in candidates
        )
        if not covers:
            failures.append(
                f"{HOLIDAY_NAME!r} span "
                f"[{holiday.date_from} -> {holiday.date_to}] does not "
                f"cover calendar day {EXPECTED_DATE} in any plausible tz "
                f"({candidates})"
            )

    return failures
