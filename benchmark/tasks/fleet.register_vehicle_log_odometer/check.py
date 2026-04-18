"""Postcondition checks for fleet.register_vehicle_log_odometer."""


PLATE = "BENCH-001"
EXPECTED_MODEL_NAME = "Model 3"
EXPECTED_BRAND_NAME = "Tesla Motors"
EXPECTED_ODOMETER_VALUE = 1250.0


def check(env):
    failures = []

    vehicles = env["fleet.vehicle"].search([("license_plate", "=", PLATE)])
    if len(vehicles) != 1:
        return [
            f"Expected exactly 1 vehicle with plate {PLATE!r}, found {len(vehicles)}"
        ]
    vehicle = vehicles[0]

    # The model must be the Tesla Model 3 seeded for this task.
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

    # There must be exactly one odometer log for this vehicle, with value 1250.
    logs = env["fleet.vehicle.odometer"].search([("vehicle_id", "=", vehicle.id)])
    if len(logs) == 0:
        failures.append(
            f"No odometer log found for vehicle {PLATE!r}; expected a log with "
            f"value {EXPECTED_ODOMETER_VALUE}"
        )
    else:
        # If multiple logs exist (e.g. agent set odometer then also created a
        # log), at least one of them must be exactly 1250.
        values = logs.mapped("value")
        if EXPECTED_ODOMETER_VALUE not in values:
            failures.append(
                f"No odometer log with value {EXPECTED_ODOMETER_VALUE} found "
                f"for vehicle {PLATE!r}; got values={values}"
            )
        if len(logs) > 1:
            # Allow at most 1 log for this easy task.
            failures.append(
                f"Expected exactly 1 odometer log for vehicle {PLATE!r}, "
                f"found {len(logs)} (values={values})"
            )

    return failures
