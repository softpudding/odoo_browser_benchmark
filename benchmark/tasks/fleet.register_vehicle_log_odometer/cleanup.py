"""Cleanup for fleet.register_vehicle_log_odometer."""


PLATE = "BENCH-001"


def cleanup(env):
    vehicles = env["fleet.vehicle"].search([("license_plate", "=", PLATE)])
    if vehicles:
        env["fleet.vehicle.odometer"].search(
            [("vehicle_id", "in", vehicles.ids)]
        ).unlink()
        vehicles.unlink()
