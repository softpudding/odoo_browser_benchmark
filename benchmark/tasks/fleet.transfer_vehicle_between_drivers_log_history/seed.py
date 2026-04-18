"""Seed for fleet.transfer_vehicle_between_drivers_log_history.

Creates two driver partners (Driver Alice, Driver Bob) and a single
fleet vehicle "Bench Sedan BS-1001" assigned to Driver Alice. The vehicle
write hook will auto-create one fleet.vehicle.assignation.log entry for
Alice (with date_start = today). The agent's job is to switch the driver
to Driver Bob, save, then edit Bob's auto-created assignation log entry
so its Start Date matches 2026-04-18.
"""


PLATE = "BS-1001"
VEHICLE_NAME = "Bench Sedan BS-1001"
ALICE = "Driver Alice"
BOB = "Driver Bob"
BRAND_NAME = "Bench Motors"
MODEL_NAME = "Bench Sedan"


def setup(env):
    # 1. Cleanup prior runs first
    vehicles = env["fleet.vehicle"].search([("license_plate", "=", PLATE)])
    if vehicles:
        env["fleet.vehicle.assignation.log"].search([("vehicle_id", "in", vehicles.ids)]).unlink()
        vehicles.unlink()

    for partner_name in (ALICE, BOB):
        partners = env["res.partner"].search([("name", "=", partner_name), ("is_company", "=", False)])
        # Only delete partners that are not referenced anywhere we care about.
        for partner in partners:
            try:
                partner.unlink()
            except Exception:
                pass

    # 2. Create driver partners (individuals, not companies)
    alice = env["res.partner"].search([("name", "=", ALICE), ("is_company", "=", False)], limit=1)
    if not alice:
        alice = env["res.partner"].create({"name": ALICE, "is_company": False})

    bob = env["res.partner"].search([("name", "=", BOB), ("is_company", "=", False)], limit=1)
    if not bob:
        bob = env["res.partner"].create({"name": BOB, "is_company": False})

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

    # 4. Create the vehicle assigned to Driver Alice. The fleet.vehicle.create
    #    hook will spawn one fleet.vehicle.assignation.log entry for Alice
    #    with date_start = today.
    env["fleet.vehicle"].create({
        "model_id": model.id,
        "license_plate": PLATE,
        "driver_id": alice.id,
    })
