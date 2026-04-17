"""Postcondition checks for fleet.log_fuel_refill_with_cost."""

from datetime import date

PLATE = "FUEL-9001"
MODEL_NAME = "Benchmark Fleet Hybrid"
SERVICE_TYPE = "Refueling"
VENDOR_NAME = "BP Express Holloway"
EXPECTED_AMOUNT = 87.50
EXPECTED_DATE = date(2026, 5, 20)


def check(env):
    failures = []

    vehicles = env["fleet.vehicle"].search([("license_plate", "=", PLATE)])
    if not vehicles:
        return [f"Vehicle '{PLATE}' not found"]
    vehicle = vehicles[0]

    # Vehicle's own fields must be unchanged (no accidental edits).
    if vehicle.model_id.name != MODEL_NAME:
        failures.append(
            f"Vehicle model changed to '{vehicle.model_id.name}', "
            f"expected '{MODEL_NAME}' (side-effect: vehicle form was edited)"
        )
    if vehicle.driver_id.name != env.ref("base.user_admin").partner_id.name:
        failures.append(
            f"Vehicle driver changed to '{vehicle.driver_id.name}', "
            f"expected unchanged"
        )

    services = env["fleet.vehicle.log.services"].search([
        ("vehicle_id", "=", vehicle.id),
    ])
    if not services:
        return failures + [
            f"No service log records on vehicle {PLATE} — the fuel refill "
            f"service was not logged"
        ]
    if len(services) > 1:
        failures.append(
            f"Expected exactly 1 service record on vehicle {PLATE}, "
            f"found {len(services)}"
        )

    svc = services[0]
    if (svc.service_type_id.name or "").strip() != SERVICE_TYPE:
        failures.append(
            f"Service type is '{svc.service_type_id.name}', expected "
            f"'{SERVICE_TYPE}'"
        )
    if (svc.vendor_id.name or "").strip() != VENDOR_NAME:
        failures.append(
            f"Vendor is '{svc.vendor_id.name}', expected '{VENDOR_NAME}'"
        )
    if abs((svc.amount or 0.0) - EXPECTED_AMOUNT) > 1e-2:
        failures.append(
            f"Amount is {svc.amount}, expected {EXPECTED_AMOUNT}"
        )
    if svc.date != EXPECTED_DATE:
        failures.append(
            f"Service date is {svc.date}, expected {EXPECTED_DATE}"
        )

    return failures
