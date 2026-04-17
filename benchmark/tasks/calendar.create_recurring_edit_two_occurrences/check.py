"""Postcondition checks for calendar.create_recurring_edit_two_occurrences.

The agent creates a weekly recurring "Cross-Team Sync" event with 6
occurrences, then edits the location of two individual occurrences
using "This Event" in the recurrence dialog. After the edits:

- June 11 occurrence: Location = "Virtual - Zoom"
- June 25 occurrence: Location = "Building B Room 201"
- All other occurrences (Jun 4, Jun 18, Jul 2, Jul 9): Location = "Main Conference Room"
- Marc Demo is an attendee
- Distractor event "Cross-Team Review" is unchanged
"""

from datetime import date


TITLE = "Cross-Team Sync"
DISTRACTOR_TITLE = "Cross-Team Review"

# (date, expected_location) for each occurrence
EXPECTED = [
    (date(2026, 6, 4), "Main Conference Room"),
    (date(2026, 6, 11), "Virtual - Zoom"),
    (date(2026, 6, 18), "Main Conference Room"),
    (date(2026, 6, 25), "Building B Room 201"),
    (date(2026, 7, 2), "Main Conference Room"),
    (date(2026, 7, 9), "Main Conference Room"),
]


def check(env):
    failures = []

    # ── 1. Find all Cross-Team Sync events ──────────────────────────
    all_events = env["calendar.event"].search(
        [("name", "=", TITLE)]
    ).sorted("start")

    if not all_events:
        return ["No 'Cross-Team Sync' events found — the event was not created"]

    # ── 2. Verify 6 occurrences exist ───────────────────────────────
    # After two "This Event" detaches, we expect:
    #   - The base recurrence may have fewer linked events
    #   - Plus 2 detached standalone events
    # Total should still be 6 calendar.event records with this name.
    if len(all_events) < 6:
        failures.append(
            f"Expected 6 'Cross-Team Sync' events (including detached), "
            f"found {len(all_events)}"
        )

    # ── 3. Check each occurrence's location ─────────────────────────
    event_dates = {}
    for event in all_events:
        event_date = event.start.date() if event.start else None
        if event_date:
            event_dates[event_date] = event

    for expected_date, expected_location in EXPECTED:
        event = event_dates.get(expected_date)
        if not event:
            failures.append(
                f"No event found on {expected_date} — occurrence may be missing"
            )
            continue
        if event.location != expected_location:
            failures.append(
                f"Event on {expected_date} has location '{event.location}', "
                f"expected '{expected_location}'"
            )

    # ── 4. Verify recurrence exists on the base event ───────────────
    base_event = event_dates.get(date(2026, 6, 4))
    if base_event:
        if not base_event.recurrency and not base_event.recurrence_id:
            failures.append(
                "Base event (Jun 4) is not marked as recurring — "
                "the event may not have been created with recurrence"
            )
        elif base_event.recurrence_id:
            rec = base_event.recurrence_id
            if rec.rrule_type != "weekly":
                failures.append(
                    f"Recurrence type is '{rec.rrule_type}', expected 'weekly'"
                )

    # ── 5. Verify Marc Demo is an attendee ──────────────────────────
    marc_found = False
    for event in all_events:
        attendee_names = set(event.partner_ids.mapped("name"))
        if "Marc Demo" in attendee_names:
            marc_found = True
            break

    if not marc_found:
        failures.append("Marc Demo is not an attendee on any Cross-Team Sync event")

    # ── 6. Verify the start time is around 10:00 ────────────────────
    if base_event:
        start_hour = base_event.start.hour
        if start_hour != 10:
            failures.append(
                f"Base event start hour is {start_hour}, expected 10 (10:00 AM UTC)"
            )

    # ── 7. Verify distractor event is unchanged ─────────────────────
    distractor_events = env["calendar.event"].search(
        [("name", "=", DISTRACTOR_TITLE)]
    )
    if not distractor_events:
        failures.append(
            f"Distractor event '{DISTRACTOR_TITLE}' was deleted — "
            f"agent may have confused it with the target event"
        )
    else:
        for de in distractor_events:
            if de.location != "Room 101":
                failures.append(
                    f"Distractor event '{DISTRACTOR_TITLE}' on {de.start.date()} "
                    f"has location '{de.location}', expected 'Room 101' (should be untouched)"
                )

    return failures
