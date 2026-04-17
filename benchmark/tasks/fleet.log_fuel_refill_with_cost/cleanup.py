"""Cleanup for fleet.log_fuel_refill_with_cost."""

PLATE = "FUEL-9001"
BRAND_NAME = "Benchmark Auto"
MODEL_NAME = "Benchmark Fleet Hybrid"


def cleanup(env):
    vehicles = env["fleet.vehicle"].search([("license_plate", "=", PLATE)])
    for v in vehicles:
        env["fleet.vehicle.log.services"].search([
            ("vehicle_id", "=", v.id),
        ]).unlink()
        env["mail.activity"].search([
            ("res_model", "=", "fleet.vehicle"),
            ("res_id", "=", v.id),
        ]).unlink()
    vehicles.unlink()
    env["fleet.vehicle.model"].search([
        ("name", "=", MODEL_NAME),
        ("brand_id.name", "=", BRAND_NAME),
    ]).unlink()
