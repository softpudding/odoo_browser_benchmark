"""Postcondition checks for fleet.schedule_vehicle_service_activity."""


PLATE = "BENCH-ACT-001"
MODEL_NAME = "Benchmark Utility Truck"
SUMMARY = "Yearly Safety Inspection"
DUE_DATE = "2026-07-20"


def check(env):
    failures = []

    vehicles = env["fleet.vehicle"].search([("license_plate", "=", PLATE)])
    if len(vehicles) != 1:
        return [f"Expected exactly 1 vehicle with plate {PLATE!r}, found {len(vehicles)}"]
    vehicle = vehicles[0]
    if vehicle.model_id.name != MODEL_NAME:
        failures.append(
            f"Vehicle model name is {vehicle.model_id.name!r}, expected {MODEL_NAME!r}"
        )

    activities = env["mail.activity"].search([
        ("res_model", "=", "fleet.vehicle"),
        ("res_id", "=", vehicle.id),
        ("summary", "=", SUMMARY),
    ])
    if len(activities) != 1:
        # Fall back: list all activities on this vehicle for easier debugging.
        all_activities = env["mail.activity"].search([
            ("res_model", "=", "fleet.vehicle"),
            ("res_id", "=", vehicle.id),
        ])
        details = ", ".join(
            f"type={a.activity_type_id.name!r}, date={a.date_deadline}, summary={a.summary!r}"
            for a in all_activities
        ) or "<none>"
        failures.append(
            f"Expected exactly 1 activity with summary {SUMMARY!r} on this vehicle, "
            f"found {len(activities)}. All activities on the vehicle: {details}"
        )
        return failures

    activity = activities[0]

    if str(activity.date_deadline) != DUE_DATE:
        failures.append(
            f"Activity due date is {activity.date_deadline!s}, expected {DUE_DATE}"
        )

    if not activity.activity_type_id:
        failures.append("Activity type is not set")
    else:
        type_name = (activity.activity_type_id.name or "").strip()
        normalized = type_name.lower().replace("-", " ").replace("_", " ")
        if normalized != "to do":
            failures.append(
                f"Activity type is {type_name!r}, expected 'To-Do' (or 'To Do')"
            )

    # Guard against scope creep: no other activities should have been created.
    other_activities = env["mail.activity"].search([
        ("res_model", "=", "fleet.vehicle"),
        ("res_id", "=", vehicle.id),
        ("id", "not in", activities.ids),
    ])
    if other_activities:
        extras = ", ".join(
            f"{a.summary!r} ({a.activity_type_id.name})" for a in other_activities
        )
        failures.append(
            f"Expected only 1 activity on this vehicle, found additional: {extras}"
        )

    return failures
