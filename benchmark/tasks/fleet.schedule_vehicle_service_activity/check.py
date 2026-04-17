"""Postcondition checks for fleet.schedule_vehicle_service_activity."""

from datetime import date

PLATE = "SVC-8812"
EXPECTED_SUMMARY = "Annual inspection and service"


def check(env):
    failures = []

    vehicles = env["fleet.vehicle"].search([("license_plate", "=", PLATE)])
    if not vehicles:
        return [f"Vehicle with plate '{PLATE}' not found"]
    vehicle = vehicles[0]

    activities = env["mail.activity"].search([
        ("res_model", "=", "fleet.vehicle"),
        ("res_id", "=", vehicle.id),
        ("summary", "=", EXPECTED_SUMMARY),
    ])
    if not activities:
        return [
            f"No open activity with summary '{EXPECTED_SUMMARY}' found on "
            f"vehicle {PLATE}"
        ]
    if len(activities) > 1:
        failures.append(f"Found {len(activities)} activities, expected 1")
    act = activities[0]

    if act.date_deadline != date(2026, 6, 30):
        failures.append(
            f"Activity due date is {act.date_deadline}, expected 2026-06-30"
        )

    return failures
