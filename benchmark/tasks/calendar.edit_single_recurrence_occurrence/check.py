"""Postcondition checks for calendar.edit_single_recurrence_occurrence.

After a "This Event" detach, Odoo creates a standalone calendar.event
for the detached occurrence. The base recurrence record still exists
but now covers one fewer occurrence. We verify:
1. A detached event exists with the new location on April 27
2. The base recurrence still has "Main Office" as location
3. No events were deleted
"""

from datetime import date


def check(env):
    failures = []

    all_events = env["calendar.event"].search([("name", "=", "Ops Standup")])

    if len(all_events) < 2:
        failures.append(
            f"Expected at least 2 'Ops Standup' DB records after detach, "
            f"found {len(all_events)}"
        )
        if not all_events:
            return failures

    target_date = date(2026, 4, 27)
    detached_found = False

    for event in all_events:
        event_date = event.start.date() if event.start else None

        if event_date == target_date:
            detached_found = True
            if event.location != "Building B Room 4":
                failures.append(
                    f"Apr 27 occurrence location is '{event.location}', "
                    f"expected 'Building B Room 4'"
                )
        else:
            # Non-target events must keep original location
            if event.location != "Main Office":
                failures.append(
                    f"Event on {event_date} has location '{event.location}', "
                    f"expected 'Main Office' (should not have been modified)"
                )

    if not detached_found:
        failures.append(
            "No event found on April 27, 2026 — the target occurrence "
            "may have been deleted instead of edited"
        )

    # Event names should all be unchanged
    for event in all_events:
        if event.name != "Ops Standup":
            failures.append(
                f"Event name changed to '{event.name}' on {event.start.date()}"
            )

    return failures
