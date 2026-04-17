"""Cleanup for fleet.schedule_vehicle_service_activity."""


PLATE = "BENCH-ACT-001"
MODEL_NAME = "Benchmark Utility Truck"
SUMMARY = "Yearly Safety Inspection"


def cleanup(env):
    vehicles = env["fleet.vehicle"].search([("license_plate", "=", PLATE)])
    if vehicles:
        env["mail.activity"].search([
            ("res_model", "=", "fleet.vehicle"),
            ("res_id", "in", vehicles.ids),
        ]).unlink()
        vehicles.unlink()

    # Also sweep any stray activities with this summary linked to fleet.vehicle
    # in case a previous run left orphans behind.
    env["mail.activity"].search([
        ("res_model", "=", "fleet.vehicle"),
        ("summary", "=", SUMMARY),
    ]).unlink()

    env["fleet.vehicle.model"].search([("name", "=", MODEL_NAME)]).unlink()
