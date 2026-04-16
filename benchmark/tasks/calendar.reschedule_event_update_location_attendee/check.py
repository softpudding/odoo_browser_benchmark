"""Postcondition checks for calendar.reschedule_event_update_location_attendee."""

from datetime import date


EVENT_NAME = "Warehouse Safety Briefing"
DISTRACTOR_NAME = "Warehouse Safety Briefing - East"


def check(env):
    failures = []

    event = env["calendar.event"].search([("name", "=", EVENT_NAME)], limit=1)
    if not event:
        return [f"Event '{EVENT_NAME}' not found"]

    if event.location != "Training Room":
        failures.append(
            f"Location is '{event.location}', expected 'Training Room'"
        )
    if event.allday:
        failures.append("Event became all-day, expected a timed event")
    if event.recurrency:
        failures.append("Event became recurring, expected one-time event")

    if not event.start or event.start.date() != date(2026, 4, 17):
        failures.append(
            f"Event date is {event.start.date() if event.start else None}, expected 2026-04-17"
        )

    attendee_names = set(event.partner_ids.mapped("name"))
    if "Marc Demo" not in attendee_names:
        failures.append("Marc Demo was not added as an attendee")

    distractor = env["calendar.event"].search(
        [("name", "=", DISTRACTOR_NAME)], limit=1
    )
    if not distractor:
        failures.append(f"Distractor event '{DISTRACTOR_NAME}' not found")
    else:
        if distractor.location != "Room 8":
            failures.append(
                f"Distractor location changed to '{distractor.location}', expected 'Room 8'"
            )
        if "Marc Demo" in set(distractor.partner_ids.mapped("name")):
            failures.append("Distractor event received the attendee change")

    return failures
