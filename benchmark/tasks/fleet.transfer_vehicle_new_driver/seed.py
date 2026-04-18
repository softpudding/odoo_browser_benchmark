"""Seed for fleet.transfer_vehicle_new_driver.

Creates two driver partners (Old Driver Bob, New Driver Alice) and a single
fleet vehicle "TESLA Model 3 [BENCH-01]" assigned to Old Driver Bob. The
fleet.vehicle.create hook auto-creates one fleet.vehicle.assignation.log
entry for Bob (with date_start = today). The agent's job is to switch the
driver to New Driver Alice, save, then set the newly created assignation
log entry's Start Date to 2026-03-15.
"""


PLATE = "BENCH-01"
OLD_DRIVER = "Old Driver Bob"
OLD_DRIVER_EMAIL = "old.bob@bench.test"
NEW_DRIVER = "New Driver Alice"
NEW_DRIVER_EMAIL = "new.alice@bench.test"
BRAND_NAME = "Tesla"
MODEL_NAME = "Model 3"


def setup(env):
    # 1. Cleanup prior runs first -- drop vehicle and its assignation logs
    vehicles = env["fleet.vehicle"].search([("license_plate", "=", PLATE)])
    if vehicles:
        env["fleet.vehicle.assignation.log"].search([("vehicle_id", "in", vehicles.ids)]).unlink()
        vehicles.unlink()

    # Drop stale model (safe now that any vehicle referencing it is gone)
    stale_models = env["fleet.vehicle.model"].search([
        ("name", "=", MODEL_NAME),
        ("brand_id.name", "=", BRAND_NAME),
    ])
    stale_models.unlink()

    # Drop stale partners by email (unique per run)
    for email in (OLD_DRIVER_EMAIL, NEW_DRIVER_EMAIL):
        partners = env["res.partner"].search([("email", "=", email)])
        for partner in partners:
            try:
                partner.unlink()
            except Exception:
                pass

    # 2. Create driver partners (individuals, not companies)
    old_driver = env["res.partner"].create({
        "name": OLD_DRIVER,
        "email": OLD_DRIVER_EMAIL,
        "is_company": False,
    })
    env["res.partner"].create({
        "name": NEW_DRIVER,
        "email": NEW_DRIVER_EMAIL,
        "is_company": False,
    })

    # 3. Brand + model so the vehicle has a recognisable display name
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

    # 4. Create the vehicle assigned to Old Driver Bob. The fleet.vehicle.create
    #    hook will spawn one fleet.vehicle.assignation.log entry for Bob with
    #    date_start = today.
    env["fleet.vehicle"].create({
        "model_id": model.id,
        "license_plate": PLATE,
        "driver_id": old_driver.id,
    })
