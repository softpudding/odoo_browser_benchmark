"""Cleanup for fleet.create_vehicle_assign_driver_contract."""


def cleanup(env):
    env["fleet.vehicle.log.contract"].search([("ins_ref", "=", "LEASE-2048")]).unlink()
    env["fleet.vehicle"].search([("license_plate", "=", "FSM-2048")]).unlink()
