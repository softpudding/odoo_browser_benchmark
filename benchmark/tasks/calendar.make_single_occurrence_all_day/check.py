"""Postcondition checks for calendar.make_single_occurrence_all_day."""

from datetime import date


def check(env):
    failures = []

    all_events = env["calendar.event"].search([("name", "=", "Warehouse Walkthrough")])
    if len(all_events) < 2:
        failures.append(
            f"Expected at least 2 'Warehouse Walkthrough' records after detach, found {len(all_events)}"
        )
        if not all_events:
            return failures

    target_date = date(2026, 5, 19)
    target_found = False

    for event in all_events:
        event_date = event.start.date() if event.start else None
        if event_date == target_date:
            target_found = True
            if event.location != "Remote Review Hub":
                failures.append(
                    f"May 19 location is {event.location!r}, expected 'Remote Review Hub'"
                )
            if not event.allday:
                failures.append("May 19 occurrence is not all-day")
            if event.follow_recurrence:
                failures.append("May 19 occurrence still follows the recurrence")
        else:
            if event.location != "North Annex":
                failures.append(
                    f"Occurrence on {event_date} has location {event.location!r}, expected 'North Annex'"
                )
            if event.allday:
                failures.append(
                    f"Occurrence on {event_date} became all-day, but only May 19 should change"
                )

    if not target_found:
        failures.append("No Warehouse Walkthrough event found on May 19, 2026")

    return failures
