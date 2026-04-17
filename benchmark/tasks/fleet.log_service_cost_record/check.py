"""Postcondition checks for fleet.log_service_cost_record."""


PLATE = "BENCH-001"
MODEL_NAME = "Benchmark Fleet Sedan"
VENDOR_NAME = "Beacon Auto Shop"


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

    services = env["fleet.vehicle.log.services"].search([
        ("vehicle_id", "=", vehicle.id),
    ])
    if len(services) != 1:
        failures.append(
            f"Expected exactly 1 service record for this vehicle, found {len(services)}"
        )
        return failures

    svc = services[0]

    if abs(svc.amount - 150.0) > 0.0001:
        failures.append(f"Service amount is {svc.amount}, expected 150.0")

    if str(svc.date) != "2026-05-10":
        failures.append(f"Service date is {svc.date!s}, expected 2026-05-10")

    if not svc.service_type_id:
        failures.append("Service type is not set")
    elif "Oil Change" not in (svc.service_type_id.name or ""):
        failures.append(
            f"Service type is {svc.service_type_id.name!r}, expected to contain 'Oil Change'"
        )

    if not svc.vendor_id:
        failures.append("Vendor is not set")
    elif svc.vendor_id.name != VENDOR_NAME:
        failures.append(
            f"Service vendor is {svc.vendor_id.name!r}, expected {VENDOR_NAME!r}"
        )

    return failures
