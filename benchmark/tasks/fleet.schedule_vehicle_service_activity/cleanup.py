"""Cleanup for fleet.schedule_vehicle_service_activity."""

PLATE = "SVC-8812"
BRAND_NAME = "Benchmark Auto"
MODEL_NAME = "Benchmark Sedan"


def cleanup(env):
    vehicles = env["fleet.vehicle"].search([("license_plate", "=", PLATE)])
    for v in vehicles:
        env["mail.activity"].search([
            ("res_model", "=", "fleet.vehicle"),
            ("res_id", "=", v.id),
        ]).unlink()
    vehicles.unlink()
    env["fleet.vehicle.model"].search([
        ("name", "=", MODEL_NAME),
        ("brand_id.name", "=", BRAND_NAME),
    ]).unlink()
    env["fleet.vehicle.model.brand"].search([("name", "=", BRAND_NAME)]).unlink()
