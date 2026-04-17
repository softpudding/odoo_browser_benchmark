"""Seed a brand and model for the fleet odometer task."""


BRAND_NAME = "Raven Motors"
MODEL_NAME = "Falcon X"
PLATE = "OPS-7421"


def setup(env):
    env["fleet.vehicle.odometer"].search([("vehicle_id.license_plate", "=", PLATE)]).unlink()
    env["fleet.vehicle"].search([("license_plate", "=", PLATE)]).unlink()

    models = env["fleet.vehicle.model"].search([("name", "=", MODEL_NAME), ("brand_id.name", "=", BRAND_NAME)])
    models.unlink()
    env["fleet.vehicle.model.brand"].search([("name", "=", BRAND_NAME)]).unlink()

    brand = env["fleet.vehicle.model.brand"].create({"name": BRAND_NAME})
    env["fleet.vehicle.model"].create({
        "name": MODEL_NAME,
        "brand_id": brand.id,
        "vehicle_type": "car",
    })
