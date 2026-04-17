"""Cleanup for fleet.create_contract_set_renewal_activity."""


def cleanup(env):
    contracts = env["fleet.vehicle.log.contract"].search([("ins_ref", "=", "RENEW-6124")])
    contracts.activity_ids.unlink()
    contracts.unlink()
    env["fleet.vehicle"].search([("license_plate", "=", "FLE-6124")]).unlink()
