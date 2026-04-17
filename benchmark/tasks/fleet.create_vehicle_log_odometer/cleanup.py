"""Cleanup for fleet.create_vehicle_log_odometer."""


def cleanup(env):
    env["fleet.vehicle.odometer"].search([("vehicle_id.license_plate", "=", "OPS-7421")]).unlink()
    env["fleet.vehicle"].search([("license_plate", "=", "OPS-7421")]).unlink()
    env["fleet.vehicle.model"].search([("name", "=", "Falcon X"), ("brand_id.name", "=", "Raven Motors")]).unlink()
    env["fleet.vehicle.model.brand"].search([("name", "=", "Raven Motors")]).unlink()
