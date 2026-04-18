"""Postcondition checks for fleet.transfer_vehicle_new_driver."""

from datetime import date


PLATE = "BENCH-01"
OLD_DRIVER = "Old Driver Bob"
NEW_DRIVER = "New Driver Alice"
NEW_START_DATE = date(2026, 3, 15)


def check(env):
    failures = []

    vehicles = env["fleet.vehicle"].search([("license_plate", "=", PLATE)])
    if len(vehicles) != 1:
        return [f"Expected exactly 1 vehicle with plate '{PLATE}', found {len(vehicles)}"]
    vehicle = vehicles[0]

    if vehicle.driver_id.name != NEW_DRIVER:
        failures.append(
            f"Vehicle driver is '{vehicle.driver_id.name}', expected '{NEW_DRIVER}'"
        )

    logs = env["fleet.vehicle.assignation.log"].search([("vehicle_id", "=", vehicle.id)])
    old_logs = logs.filtered(lambda r: r.driver_id.name == OLD_DRIVER)
    new_logs = logs.filtered(lambda r: r.driver_id.name == NEW_DRIVER)

    if not old_logs:
        failures.append(
            f"No assignation log entry found for original driver '{OLD_DRIVER}'"
        )
    else:
        # The old driver's assignation log should have been closed
        # (date_end set) when we switched drivers.
        if not any(log.date_end for log in old_logs):
            failures.append(
                f"'{OLD_DRIVER}' assignation log was not closed (date_end is empty)"
            )

    if len(new_logs) != 1:
        failures.append(
            f"Expected exactly 1 assignation log entry for '{NEW_DRIVER}', found {len(new_logs)}"
        )
        return failures

    new_log = new_logs[0]
    if not new_log.date_start:
        failures.append(f"'{NEW_DRIVER}' assignation log has no Start Date")
    elif new_log.date_start != NEW_START_DATE:
        failures.append(
            f"'{NEW_DRIVER}' assignation log Start Date is {new_log.date_start}, "
            f"expected {NEW_START_DATE}"
        )

    return failures
