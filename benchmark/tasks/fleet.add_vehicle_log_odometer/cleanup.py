"""Cleanup for fleet.add_vehicle_log_odometer."""


PLATE = "FLEET-ADD-01"


def cleanup(env):
    vehicles = env["fleet.vehicle"].search([("license_plate", "=", PLATE)])
    if vehicles:
        env["fleet.vehicle.odometer"].search(
            [("vehicle_id", "in", vehicles.ids)]
        ).unlink()
        vehicles.unlink()
