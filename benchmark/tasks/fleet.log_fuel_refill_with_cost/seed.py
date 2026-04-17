"""Seed for fleet.log_fuel_refill_with_cost.

Creates vehicle FUEL-9001 (Benchmark Fleet Hybrid, driver = admin).
No existing service records. Task is to add a fuel refill service.
"""

BRAND_NAME = "Benchmark Auto"
MODEL_NAME = "Benchmark Fleet Hybrid"
PLATE = "FUEL-9001"


def setup(env):
    # Cleanup prior runs.
    vehicle = env["fleet.vehicle"].search([("license_plate", "=", PLATE)], limit=1)
    if vehicle:
        env["fleet.vehicle.log.services"].search([
            ("vehicle_id", "=", vehicle.id),
        ]).unlink()
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
            "default_fuel_type": "full_hybrid",
        })

    admin = env.ref("base.user_admin")
    env["fleet.vehicle"].create({
        "model_id": model.id,
        "license_plate": PLATE,
        "driver_id": admin.partner_id.id,
    })

    # Pre-create the Refueling service type and the vendor so that the
    # oracle (and browser-use) can select them without triggering the
    # on-the-fly quick-create dialog.
    st = env["fleet.service.type"].search([("name", "=", "Refueling")], limit=1)
    if not st:
        env["fleet.service.type"].create({
            "name": "Refueling",
            "category": "service",
        })
    vendor = env["res.partner"].search([
        ("name", "=", "BP Express Holloway"),
    ], limit=1)
    if not vendor:
        env["res.partner"].create({
            "name": "BP Express Holloway",
            "supplier_rank": 1,
        })
