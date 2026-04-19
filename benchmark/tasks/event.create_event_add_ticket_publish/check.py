"""Postcondition checks for event.create_event_add_ticket_publish."""

from datetime import datetime


EVENT_NAME = "Bench Summer Summit 2026"
TICKET_NAME = "General Admission"
TICKET_PRICE = 50.0

# Prompt-declared local wall-clock times.
EXPECTED_BEGIN_LOCAL = datetime(2026, 6, 15, 9, 0, 0)
EXPECTED_END_LOCAL = datetime(2026, 6, 15, 17, 0, 0)


def _admin_tz(env):
    import pytz

    admin = env["res.users"].search([("login", "=", "admin")], limit=1)
    tz_name = (admin.tz if admin else None) or env.user.tz or "UTC"
    try:
        return pytz.timezone(tz_name)
    except Exception:
        return pytz.UTC


def _utc_to_local_naive(env, dt):
    """Convert a naive UTC datetime (as stored in Odoo) to a naive
    datetime in the admin's local timezone so we can compare against
    the prompt's wall-clock targets."""
    import pytz

    if dt is None:
        return None
    tz = _admin_tz(env)
    return pytz.UTC.localize(dt).astimezone(tz).replace(tzinfo=None)


def check(env):
    failures = []

    events = env["event.event"].with_context(active_test=False).search([
        ("name", "=", EVENT_NAME),
    ])
    if len(events) != 1:
        return [
            f"Expected exactly 1 event named '{EVENT_NAME}', found {len(events)}"
        ]
    event = events[0]

    begin_local = _utc_to_local_naive(env, event.date_begin)
    end_local = _utc_to_local_naive(env, event.date_end)
    if begin_local != EXPECTED_BEGIN_LOCAL:
        failures.append(
            f"Event start (local) is {begin_local}, expected {EXPECTED_BEGIN_LOCAL}"
        )
    if end_local != EXPECTED_END_LOCAL:
        failures.append(
            f"Event end (local) is {end_local}, expected {EXPECTED_END_LOCAL}"
        )

    if not event.is_published:
        failures.append("Event is_published is False — expected True")

    tickets = event.event_ticket_ids
    if len(tickets) != 1:
        failures.append(
            f"Expected exactly 1 ticket on '{EVENT_NAME}', found {len(tickets)}: "
            f"{tickets.mapped('name')}"
        )
        return failures

    ticket = tickets[0]
    if (ticket.name or "").strip() != TICKET_NAME:
        failures.append(
            f"Ticket name is {ticket.name!r}, expected {TICKET_NAME!r}"
        )
    if abs(ticket.price - TICKET_PRICE) > 0.0001:
        failures.append(
            f"Ticket price is {ticket.price}, expected {TICKET_PRICE}"
        )

    # Guardrail: no extra events with the same name (search above returned exactly 1).
    return failures
