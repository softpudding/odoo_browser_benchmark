"""Seed for fleet.schedule_vehicle_service_activity.

Creates a specific fleet vehicle SVC-8812. The task is to schedule a
To-Do activity on it with a specific summary and date.
"""

BRAND_NAME = "Benchmark Auto"
MODEL_NAME = "Benchmark Sedan"
PLATE = "SVC-8812"


def setup(env):
    # Clean any prior activities on this vehicle.
    vehicle = env["fleet.vehicle"].search([("license_plate", "=", PLATE)], limit=1)
    if vehicle:
        env["mail.activity"].search([
            ("res_model", "=", "fleet.vehicle"),
            ("res_id", "=", vehicle.id),
        ]).unlink()

    env["fleet.vehicle"].search([("license_plate", "=", PLATE)]).unlink()

    brand = env["fleet.vehicle.model.brand"].search([("name", "=", BRAND_NAME)], limit=1)
    if not brand:
        brand = env["fleet.vehicle.model.brand"].create({"name": BRAND_NAME})
    model = env["fleet.vehicle.model"].search([
        ("name", "=", MODEL_NAME),
        ("brand_id", "=", brand.id),
    ], limit=1)
    if not model:
        model = env["fleet.vehicle.model"].create({
            "name": MODEL_NAME,
            "brand_id": brand.id,
            "vehicle_type": "car",
        })

    env["fleet.vehicle"].create({
        "model_id": model.id,
        "license_plate": PLATE,
        "driver_id": env.ref("base.user_admin").partner_id.id,
    })
