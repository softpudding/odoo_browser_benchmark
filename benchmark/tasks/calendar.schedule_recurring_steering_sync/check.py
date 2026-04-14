"""Postcondition checks for calendar.schedule_recurring_steering_sync."""


TITLE = "Northwind Steering Sync"
EXPECTED_DATES = ["2026-05-07", "2026-05-14", "2026-05-21"]
EXPECTED_LOCATIONS = ["War Room B", "War Room C", "War Room B"]


def check(env):
    failures = []
    events = env["calendar.event"].search([("name", "=", TITLE)]).sorted("start")

    if len(events) != 3:
        return [f"Expected exactly 3 recurring events, found {len(events)}"]

    for event, expected_date, expected_location in zip(events, EXPECTED_DATES, EXPECTED_LOCATIONS):
        if str(event.start.date()) != expected_date:
            failures.append(
                f"Event date is {event.start.date()!r}, expected {expected_date!r}"
            )
        duration_minutes = int((event.stop - event.start).total_seconds() / 60)
        if duration_minutes != 45:
            failures.append(
                f"Event duration is {duration_minutes} minutes, expected 45"
            )
        if event.location != expected_location:
            failures.append(
                f"Event on {expected_date} has location {event.location!r}, expected {expected_location!r}"
            )
        if "Escalate blockers before launch freeze." not in (event.description or ""):
            failures.append(
                f"Event description is {event.description!r}, expected scheduling note content"
            )
        if event.allday:
            failures.append("Event was created as all-day, expected timed meeting")

    base = events[0]
    if not base.recurrency:
        failures.append("Base event is not marked recurrent")
    if not base.recurrence_id:
        failures.append("Base event has no recurrence rule")
    else:
        if base.rrule_type != "weekly":
            failures.append(f"Recurrence type is {base.rrule_type!r}, expected 'weekly'")
        if int(base.count or 0) != 3:
            failures.append(f"Recurrence count is {base.count!r}, expected 3")
        if len(base.recurrence_id.calendar_event_ids) != 3:
            failures.append(
                f"Recurrence generated {len(base.recurrence_id.calendar_event_ids)} events, expected 3"
            )

    attendee_names = set(base.partner_ids.mapped("name"))
    if "Avery Stone" not in attendee_names:
        failures.append("Avery Stone is not invited to the meeting")
    if any("Morgan Tate" in set(event.partner_ids.mapped("name")) for event in events):
        failures.append("Morgan Tate was invited, expected to stay excluded")

    return failures
