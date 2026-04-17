"""Postcondition checks for fleet.create_vehicle_log_odometer."""


BRAND_NAME = "Raven Motors"
MODEL_NAME = "Falcon X"
PLATE = "OPS-7421"


def check(env):
    failures = []

    vehicles = env["fleet.vehicle"].search([("license_plate", "=", PLATE)])
    if len(vehicles) != 1:
        return [f"Expected exactly 1 vehicle with plate '{PLATE}', found {len(vehicles)}"]

    vehicle = vehicles[0]
    if vehicle.model_id.name != MODEL_NAME or vehicle.model_id.brand_id.name != BRAND_NAME:
        failures.append(
            f"Vehicle model is '{vehicle.model_id.display_name}', expected '{BRAND_NAME}/{MODEL_NAME}'"
        )
    if vehicle.driver_id.display_name != "OdooBot":
        failures.append(
            f"Vehicle driver is '{vehicle.driver_id.display_name}', expected 'OdooBot'"
        )
    if abs(vehicle.odometer - 12540.0) > 0.0001:
        failures.append(f"Vehicle odometer is {vehicle.odometer}, expected 12540.0")

    logs = env["fleet.vehicle.odometer"].search([
        ("vehicle_id", "=", vehicle.id),
        ("value", "=", 12540.0),
    ])
    if len(logs) != 1:
        failures.append(f"Expected exactly 1 odometer log at 12540.0, found {len(logs)}")

    return failures
