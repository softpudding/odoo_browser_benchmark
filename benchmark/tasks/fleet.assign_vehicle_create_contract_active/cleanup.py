"""Cleanup for fleet.assign_vehicle_create_contract_active."""


PLATE = "BENCH-VAN-01"
MODEL_NAME = "Bench Van"
VENDOR_NAME = "Bench Lease Co"
DRIVER_NAME = "Bench Driver Partner"


def cleanup(env):
    vehicles = env["fleet.vehicle"].with_context(active_test=False).search([
        ("license_plate", "=", PLATE),
    ])
    if vehicles:
        env["fleet.vehicle.log.contract"].with_context(active_test=False).search([
            ("vehicle_id", "in", vehicles.ids),
        ]).unlink()
        env["fleet.vehicle.log.services"].with_context(active_test=False).search([
            ("vehicle_id", "in", vehicles.ids),
        ]).unlink()
        env["fleet.vehicle.odometer"].search([
            ("vehicle_id", "in", vehicles.ids),
        ]).unlink()
        env["fleet.vehicle.assignation.log"].search([
            ("vehicle_id", "in", vehicles.ids),
        ]).unlink()
        env["mail.activity"].search([
            ("res_model", "=", "fleet.vehicle"),
            ("res_id", "in", vehicles.ids),
        ]).unlink()
        vehicles.unlink()

    env["fleet.vehicle.model"].search([("name", "=", MODEL_NAME)]).unlink()
    env["res.partner"].with_context(active_test=False).search([
        ("name", "in", [VENDOR_NAME, DRIVER_NAME]),
    ]).unlink()
