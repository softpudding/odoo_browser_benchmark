"""Seed for fleet.create_vehicle_log_odometer.

Category 2 (MEDIUM): Create a vehicle and log an odometer reading.
The agent must navigate the Fleet UI, create a vehicle with specific details,
then find and use the odometer logging feature.
"""

LICENSE_PLATE = "BENCH-FL-01"


def setup(env):
    # Cleanup prior runs
    old_vehicles = env["fleet.vehicle"].search([
        ("license_plate", "=", LICENSE_PLATE),
    ])
    if old_vehicles:
        # Delete odometer entries first
        env["fleet.vehicle.odometer"].search([
            ("vehicle_id", "in", old_vehicles.ids),
        ]).unlink()
        old_vehicles.unlink()

    # Ensure Audi brand exists (should be pre-installed)
    brand = env["fleet.vehicle.model.brand"].search(
        [("name", "=", "Audi")], limit=1
    )
    if not brand:
        brand = env["fleet.vehicle.model.brand"].create({"name": "Audi"})

    # Ensure A4 model exists under Audi
    model = env["fleet.vehicle.model"].search([
        ("name", "=", "A4"),
        ("brand_id", "=", brand.id),
    ], limit=1)
    if not model:
        env["fleet.vehicle.model"].create({
            "name": "A4",
            "brand_id": brand.id,
        })
