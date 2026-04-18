"""Seed data for fleet.register_vehicle_log_odometer.

Prepares:
  - Tesla Motors brand (already seeded via fleet/data/fleet_cars_data.xml,
    but we ensure it exists defensively).
  - A fleet.vehicle.model named "Model 3" under the Tesla brand, so the
    agent can select "Tesla/Model 3" from the model many2one without
    having to create a brand/model from scratch (easy difficulty).

Cleans up prior runs:
  - Removes any fleet.vehicle with license_plate == "BENCH-001".
  - Removes any fleet.vehicle.odometer log pointing at those vehicles.
  - Does NOT delete the brand or model — they are reusable fixtures.
"""


PLATE = "BENCH-001"
BRAND_NAME = "Tesla Motors"
MODEL_NAME = "Model 3"


def setup(env):
    Vehicle = env["fleet.vehicle"]
    Odometer = env["fleet.vehicle.odometer"]
    Brand = env["fleet.vehicle.model.brand"]
    Model = env["fleet.vehicle.model"]

    # --- Cleanup prior runs ---
    stale_vehicles = Vehicle.search([("license_plate", "=", PLATE)])
    if stale_vehicles:
        Odometer.search([("vehicle_id", "in", stale_vehicles.ids)]).unlink()
        stale_vehicles.unlink()

    # --- Ensure brand exists (Tesla Motors is in fleet data, but be safe) ---
    brand = Brand.search([("name", "=", BRAND_NAME)], limit=1)
    if not brand:
        brand = Brand.create({"name": BRAND_NAME})

    # --- Ensure the "Model 3" model exists under Tesla ---
    model = Model.search(
        [("name", "=", MODEL_NAME), ("brand_id", "=", brand.id)], limit=1
    )
    if not model:
        Model.create({
            "name": MODEL_NAME,
            "brand_id": brand.id,
            "vehicle_type": "car",
        })
