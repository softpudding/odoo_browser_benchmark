"""Postcondition checks for fleet.create_vehicle_log_odometer.

Validates:
1. A vehicle exists with license plate BENCH-FL-01.
2. The vehicle's model brand is Audi.
3. An odometer entry exists with value 15200.
"""

LICENSE_PLATE = "BENCH-FL-01"


def check(env):
    failures = []

    vehicle = env["fleet.vehicle"].search([
        ("license_plate", "=", LICENSE_PLATE),
    ], limit=1)
    if not vehicle:
        return [f"No vehicle found with license plate '{LICENSE_PLATE}'"]

    # Check brand
    if vehicle.model_id and vehicle.model_id.brand_id:
        if vehicle.model_id.brand_id.name != "Audi":
            failures.append(
                f"Vehicle brand is '{vehicle.model_id.brand_id.name}', expected 'Audi'"
            )
    else:
        failures.append("Vehicle has no model/brand set")

    # Check driver
    if vehicle.driver_id:
        if vehicle.driver_id.name != "Mitchell Admin":
            failures.append(
                f"Vehicle driver is '{vehicle.driver_id.name}', expected 'Mitchell Admin'"
            )
    else:
        failures.append("Vehicle has no driver assigned")

    # Check odometer
    odometer_entries = env["fleet.vehicle.odometer"].search([
        ("vehicle_id", "=", vehicle.id),
    ])
    if not odometer_entries:
        failures.append("No odometer entries found for the vehicle")
    else:
        has_correct = any(
            abs(entry.value - 15200.0) < 0.01 for entry in odometer_entries
        )
        if not has_correct:
            values = [e.value for e in odometer_entries]
            failures.append(
                f"No odometer entry with value 15200; found: {values}"
            )

    return failures
