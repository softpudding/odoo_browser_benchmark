"""Postcondition checks for fleet.transfer_vehicle_between_drivers_log_history."""

from datetime import date, timedelta


PLATE = "BS-1001"
ALICE = "Driver Alice"
BOB = "Driver Bob"
BOB_DATE = date(2026, 4, 18)


def check(env):
    failures = []

    vehicles = env["fleet.vehicle"].search([("license_plate", "=", PLATE)])
    if len(vehicles) != 1:
        return [f"Expected exactly 1 vehicle with plate '{PLATE}', found {len(vehicles)}"]
    vehicle = vehicles[0]

    if vehicle.driver_id.name != BOB:
        failures.append(
            f"Vehicle driver is '{vehicle.driver_id.name}', expected '{BOB}'"
        )

    logs = env["fleet.vehicle.assignation.log"].search([("vehicle_id", "=", vehicle.id)])
    bob_logs = logs.filtered(lambda r: r.driver_id.name == BOB)
    alice_logs = logs.filtered(lambda r: r.driver_id.name == ALICE)

    if not alice_logs:
        failures.append(
            "No assignation log entry found for original driver 'Driver Alice'"
        )

    if len(bob_logs) != 1:
        failures.append(
            f"Expected exactly 1 assignation log entry for 'Driver Bob', found {len(bob_logs)}"
        )
        return failures

    bob_log = bob_logs[0]
    if not bob_log.date_start:
        failures.append("Driver Bob's assignation log has no Start Date")
    else:
        delta = abs((bob_log.date_start - BOB_DATE).days)
        if delta > 1:
            failures.append(
                f"Driver Bob's assignation log Start Date is {bob_log.date_start}, "
                f"expected within 1 day of {BOB_DATE}"
            )

    return failures
