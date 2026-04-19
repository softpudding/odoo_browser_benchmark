"""Postcondition checks for fleet.add_vehicle_log_odometer."""

from datetime import date


PLATE = "FLEET-ADD-01"
EXPECTED_MODEL_NAME = "Model 3"
EXPECTED_BRAND_NAME = "Tesla Motors"
EXPECTED_ODOMETER_VALUE = 15000.0
EXPECTED_DATE = date(2026, 4, 15)


def check(env):
    failures = []

    vehicles = env["fleet.vehicle"].search([("license_plate", "=", PLATE)])
    if len(vehicles) != 1:
        return [
            f"Expected exactly 1 vehicle with plate {PLATE!r}, found {len(vehicles)}"
        ]
    vehicle = vehicles[0]

    # The model must be the Tesla Motors/Model 3 seeded for this task.
    model = vehicle.model_id
    if not model:
        failures.append("Vehicle has no model set")
    else:
        if model.name != EXPECTED_MODEL_NAME:
            failures.append(
                f"Vehicle model is {model.name!r}, expected {EXPECTED_MODEL_NAME!r}"
            )
        if not model.brand_id or model.brand_id.name != EXPECTED_BRAND_NAME:
            brand_name = model.brand_id.name if model.brand_id else None
            failures.append(
                f"Vehicle brand is {brand_name!r}, expected {EXPECTED_BRAND_NAME!r}"
            )

    # There must be exactly one odometer log with value 15000 on 2026-04-15.
    logs = env["fleet.vehicle.odometer"].search([("vehicle_id", "=", vehicle.id)])
    if len(logs) == 0:
        failures.append(
            f"No odometer log found for vehicle {PLATE!r}; expected a log with "
            f"value {EXPECTED_ODOMETER_VALUE} on {EXPECTED_DATE.isoformat()}"
        )
    else:
        matching = logs.filtered(
            lambda l: abs(l.value - EXPECTED_ODOMETER_VALUE) < 0.0001
            and l.date == EXPECTED_DATE
        )
        if len(matching) != 1:
            failures.append(
                f"Expected exactly 1 odometer log with value "
                f"{EXPECTED_ODOMETER_VALUE} on {EXPECTED_DATE.isoformat()} for "
                f"vehicle {PLATE!r}, found {len(matching)} matching "
                f"(total logs={len(logs)}, "
                f"values={logs.mapped('value')}, dates={[d.isoformat() for d in logs.mapped('date')]})"
            )
        if len(logs) > 1:
            failures.append(
                f"Expected exactly 1 odometer log for vehicle {PLATE!r}, "
                f"found {len(logs)}"
            )

    return failures
