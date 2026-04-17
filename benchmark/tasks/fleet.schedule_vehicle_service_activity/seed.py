"""Seed data for fleet.schedule_vehicle_service_activity.

Creates a single vehicle "Benchmark Utility Truck" with license plate
BENCH-ACT-001 and brand "Ford". The agent must schedule a To-Do activity
on this vehicle via the chatter.
"""


VEHICLE_LABEL = "Benchmark Utility Truck"  # used as the fleet.vehicle.model name
PLATE = "BENCH-ACT-001"
BRAND_NAME = "Ford"
MODEL_NAME = VEHICLE_LABEL
SUMMARY = "Yearly Safety Inspection"


def setup(env):
    Vehicle = env["fleet.vehicle"]
    Activity = env["mail.activity"]
    Brand = env["fleet.vehicle.model.brand"]
    Model = env["fleet.vehicle.model"]

    # --- Cleanup prior runs ---
    stale_vehicles = Vehicle.search([("license_plate", "=", PLATE)])
    if stale_vehicles:
        Activity.search([
            ("res_model", "=", "fleet.vehicle"),
            ("res_id", "in", stale_vehicles.ids),
        ]).unlink()
        stale_vehicles.unlink()

    # Drop any stale model with the same label (safe since we just removed
    # any vehicle using it).
    stale_models = Model.search([("name", "=", MODEL_NAME)])
    stale_models.unlink()

    # --- Ensure brand + model exist ---
    brand = Brand.search([("name", "=", BRAND_NAME)], limit=1)
    if not brand:
        brand = Brand.create({"name": BRAND_NAME})

    model = Model.search([
        ("name", "=", MODEL_NAME),
        ("brand_id", "=", brand.id),
    ], limit=1)
    if not model:
        model = Model.create({
            "name": MODEL_NAME,
            "brand_id": brand.id,
            "vehicle_type": "car",
        })

    # --- Create the vehicle ---
    # The `name` field is computed (Brand/Model/Plate), so we encode
    # "Benchmark Utility Truck" into the model name instead. The resulting
    # vehicle name is "Ford/Benchmark Utility Truck/BENCH-ACT-001".
    admin_partner = env.ref("base.partner_admin", raise_if_not_found=False)
    vals = {
        "license_plate": PLATE,
        "model_id": model.id,
    }
    if admin_partner:
        vals["driver_id"] = admin_partner.id
    Vehicle.create(vals)
