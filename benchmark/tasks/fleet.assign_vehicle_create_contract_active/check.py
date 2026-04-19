"""Postcondition checks for fleet.assign_vehicle_create_contract_active."""


PLATE = "BENCH-VAN-01"
MODEL_NAME = "Bench Van"
VENDOR_NAME = "Bench Lease Co"
CONTRACT_TYPE_NAME = "Leasing"
EXPECTED_COST_GENERATED = 200.0
EXPECTED_FREQUENCY = "monthly"
EXPECTED_START_DATE = "2026-04-20"
EXPECTED_STATE = "open"


def check(env):
    failures = []

    vehicles = env["fleet.vehicle"].with_context(active_test=False).search([
        ("license_plate", "=", PLATE),
    ])
    if len(vehicles) != 1:
        return [
            f"Expected exactly 1 vehicle with plate {PLATE!r}, found {len(vehicles)}"
        ]
    vehicle = vehicles[0]
    if not vehicle.model_id or vehicle.model_id.name != MODEL_NAME:
        failures.append(
            f"Vehicle model is {vehicle.model_id.name!r}, expected {MODEL_NAME!r}"
        )

    # Exactly one contract linked to this vehicle.
    contracts = env["fleet.vehicle.log.contract"].with_context(active_test=False).search([
        ("vehicle_id", "=", vehicle.id),
    ])
    if len(contracts) != 1:
        failures.append(
            f"Expected exactly 1 contract for {PLATE!r}, found {len(contracts)}"
        )
        if not contracts:
            return failures

    ct = contracts[0]

    if not ct.cost_subtype_id:
        failures.append("Contract Type (cost_subtype_id) is not set")
    elif ct.cost_subtype_id.name != CONTRACT_TYPE_NAME:
        failures.append(
            f"Contract type is {ct.cost_subtype_id.name!r}, expected {CONTRACT_TYPE_NAME!r}"
        )

    if not ct.insurer_id:
        failures.append("Contract vendor (insurer_id) is not set")
    elif ct.insurer_id.name != VENDOR_NAME:
        failures.append(
            f"Contract vendor is {ct.insurer_id.name!r}, expected {VENDOR_NAME!r}"
        )

    if abs(ct.cost_generated - EXPECTED_COST_GENERATED) > 0.0001:
        failures.append(
            f"Recurring Cost is {ct.cost_generated}, expected {EXPECTED_COST_GENERATED}"
        )

    if ct.cost_frequency != EXPECTED_FREQUENCY:
        failures.append(
            f"Cost frequency is {ct.cost_frequency!r}, expected {EXPECTED_FREQUENCY!r}"
        )

    if str(ct.start_date) != EXPECTED_START_DATE:
        failures.append(
            f"Start date is {ct.start_date!s}, expected {EXPECTED_START_DATE}"
        )

    if ct.state != EXPECTED_STATE:
        failures.append(
            f"Contract state is {ct.state!r}, expected {EXPECTED_STATE!r}"
        )

    # The vehicle must remain active and linked to the seeded driver.
    if not vehicle.driver_id:
        failures.append("Vehicle driver was cleared")
    if vehicle.license_plate != PLATE:
        failures.append(
            f"Vehicle plate is {vehicle.license_plate!r}, expected {PLATE!r}"
        )

    return failures
