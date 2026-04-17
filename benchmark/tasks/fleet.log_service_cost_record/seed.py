"""Seed data for fleet.log_service_cost_record.

Creates a single vehicle "Benchmark Fleet Sedan" with license plate BENCH-001
and a vendor partner "Beacon Auto Shop". The agent must log a service
record against this vehicle via the UI. The Oil Change service type is
ensured to exist (since it is only installed by demo data, which the
benchmark snapshot may lack).
"""


VEHICLE_LABEL = "Benchmark Fleet Sedan"  # used as the fleet.vehicle.model name
PLATE = "BENCH-001"
BRAND_NAME = "Toyota"
MODEL_NAME = VEHICLE_LABEL
VENDOR_NAME = "Beacon Auto Shop"
SERVICE_TYPE_NAME = "Oil Change"


def setup(env):
    Vehicle = env["fleet.vehicle"]
    Service = env["fleet.vehicle.log.services"]
    Partner = env["res.partner"]
    Brand = env["fleet.vehicle.model.brand"]
    Model = env["fleet.vehicle.model"]
    ServiceType = env["fleet.service.type"]

    # --- Cleanup prior runs ---
    stale_vehicles = Vehicle.search([("license_plate", "=", PLATE)])
    if stale_vehicles:
        Service.search([("vehicle_id", "in", stale_vehicles.ids)]).unlink()
        stale_vehicles.unlink()

    # Drop any stale model with the same label (safe since we just removed
    # any vehicle using it).
    stale_models = Model.search([("name", "=", MODEL_NAME)])
    stale_models.unlink()

    Partner.search([("name", "=", VENDOR_NAME)]).unlink()

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

    # --- Ensure Oil Change service type exists ---
    service_type = ServiceType.search([
        ("name", "=", SERVICE_TYPE_NAME),
        ("category", "=", "service"),
    ], limit=1)
    if not service_type:
        ServiceType.create({
            "name": SERVICE_TYPE_NAME,
            "category": "service",
        })

    # --- Create vendor partner ---
    Partner.create({
        "name": VENDOR_NAME,
        "supplier_rank": 1,
    })

    # --- Create the vehicle ---
    # The `name` field is computed (Brand/Model/Plate), so we encode
    # "Benchmark Fleet Sedan" into the model name instead. The resulting
    # vehicle name is "Toyota/Benchmark Fleet Sedan/BENCH-001".
    admin_partner = env.ref("base.partner_admin", raise_if_not_found=False)
    vals = {
        "license_plate": PLATE,
        "model_id": model.id,
    }
    if admin_partner:
        vals["driver_id"] = admin_partner.id
    Vehicle.create(vals)
