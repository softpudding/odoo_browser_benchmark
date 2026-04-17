"""Cleanup for fleet.log_service_cost_record."""


PLATE = "BENCH-001"
MODEL_NAME = "Benchmark Fleet Sedan"
VENDOR_NAME = "Beacon Auto Shop"


def cleanup(env):
    vehicles = env["fleet.vehicle"].search([("license_plate", "=", PLATE)])
    if vehicles:
        env["fleet.vehicle.log.services"].search([
            ("vehicle_id", "in", vehicles.ids),
        ]).unlink()
        vehicles.unlink()

    env["fleet.vehicle.model"].search([("name", "=", MODEL_NAME)]).unlink()
    env["res.partner"].search([("name", "=", VENDOR_NAME)]).unlink()
