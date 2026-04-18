"""Postcondition checks for fleet.log_service_cost_add_odometer_close."""


PLATE = "BENCH-TRUCK-01"
MODEL_NAME = "Benchmark Truck"
VENDOR_NAME = "Bench Garage"
SERVICE_TYPE_NAME = "Oil Change"
EXPECTED_AMOUNT = 120.0
EXPECTED_DATE = "2026-04-15"
EXPECTED_ODOMETER_VALUE = 25000.0
EXPECTED_STATE = "done"


def check(env):
    failures = []

    vehicles = env["fleet.vehicle"].search([("license_plate", "=", PLATE)])
    if len(vehicles) != 1:
        return [
            f"Expected exactly 1 vehicle with plate {PLATE!r}, found {len(vehicles)}"
        ]
    vehicle = vehicles[0]
    if not vehicle.model_id or vehicle.model_id.name != MODEL_NAME:
        failures.append(
            f"Vehicle model is {vehicle.model_id.name!r}, expected {MODEL_NAME!r}"
        )

    # Exactly one service record linked to the vehicle.
    services = env["fleet.vehicle.log.services"].search([
        ("vehicle_id", "=", vehicle.id),
    ])
    if len(services) != 1:
        failures.append(
            f"Expected exactly 1 service record for {PLATE!r}, found {len(services)}"
        )
        if not services:
            return failures

    svc = services[0]

    if not svc.service_type_id:
        failures.append("Service type is not set")
    elif svc.service_type_id.name != SERVICE_TYPE_NAME:
        failures.append(
            f"Service type is {svc.service_type_id.name!r}, expected {SERVICE_TYPE_NAME!r}"
        )

    if abs(svc.amount - EXPECTED_AMOUNT) > 0.0001:
        failures.append(f"Service amount is {svc.amount}, expected {EXPECTED_AMOUNT}")

    if str(svc.date) != EXPECTED_DATE:
        failures.append(f"Service date is {svc.date!s}, expected {EXPECTED_DATE}")

    if not svc.vendor_id:
        failures.append("Vendor is not set")
    elif svc.vendor_id.name != VENDOR_NAME:
        failures.append(
            f"Service vendor is {svc.vendor_id.name!r}, expected {VENDOR_NAME!r}"
        )

    if svc.state != EXPECTED_STATE:
        failures.append(
            f"Service state is {svc.state!r}, expected {EXPECTED_STATE!r}"
        )

    # Description/notes must be empty-ish (prompt explicitly says leave empty).
    if svc.description:
        failures.append(f"Service description is {svc.description!r}, expected empty")
    if svc.notes:
        failures.append(f"Service notes is {svc.notes!r}, expected empty")

    # At least one odometer reading with value 25000 must exist for this vehicle.
    # Filling the odometer field on a service auto-creates an fleet.vehicle.odometer.
    odo_logs = env["fleet.vehicle.odometer"].search([
        ("vehicle_id", "=", vehicle.id),
    ])
    values = odo_logs.mapped("value")
    if EXPECTED_ODOMETER_VALUE not in values:
        failures.append(
            f"No odometer reading with value {EXPECTED_ODOMETER_VALUE} for vehicle "
            f"{PLATE!r}; got values={values}"
        )
    # Allow at most 1 odometer log (filling the service's odometer field
    # creates exactly one; creating a separate one would double up).
    if len(odo_logs) > 1:
        failures.append(
            f"Expected exactly 1 odometer log for {PLATE!r}, found {len(odo_logs)} "
            f"(values={values})"
        )

    return failures
