"""Cleanup for fleet.log_service_cost_add_odometer_close."""


PLATE = "BENCH-TRUCK-01"
MODEL_NAME = "Benchmark Truck"
VENDOR_NAME = "Bench Garage"


def cleanup(env):
    vehicles = env["fleet.vehicle"].with_context(active_test=False).search([
        ("license_plate", "=", PLATE),
    ])
    if vehicles:
        env["fleet.vehicle.log.services"].with_context(active_test=False).search([
            ("vehicle_id", "in", vehicles.ids),
        ]).unlink()
        env["fleet.vehicle.odometer"].search([
            ("vehicle_id", "in", vehicles.ids),
        ]).unlink()
        env["mail.activity"].search([
            ("res_model", "=", "fleet.vehicle"),
            ("res_id", "in", vehicles.ids),
        ]).unlink()
        vehicles.unlink()

    env["fleet.vehicle.model"].search([("name", "=", MODEL_NAME)]).unlink()
    env["res.partner"].with_context(active_test=False).search([
        ("name", "=", VENDOR_NAME),
    ]).unlink()
