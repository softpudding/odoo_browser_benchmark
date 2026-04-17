"""Clean up artifacts from previous runs."""

LICENSE_PLATE = "BENCH-FL-01"


def cleanup(env):
    vehicles = env["fleet.vehicle"].search([
        ("license_plate", "=", LICENSE_PLATE),
    ])
    if vehicles:
        env["fleet.vehicle.odometer"].search([
            ("vehicle_id", "in", vehicles.ids),
        ]).unlink()
        vehicles.unlink()
