"""Cleanup for fleet.transfer_vehicle_between_drivers_log_history."""


PLATE = "BS-1001"
ALICE = "Driver Alice"
BOB = "Driver Bob"


def cleanup(env):
    vehicles = env["fleet.vehicle"].search([("license_plate", "=", PLATE)])
    if vehicles:
        env["fleet.vehicle.assignation.log"].search([("vehicle_id", "in", vehicles.ids)]).unlink()
        vehicles.unlink()
    for partner_name in (ALICE, BOB):
        partners = env["res.partner"].search([("name", "=", partner_name), ("is_company", "=", False)])
        for partner in partners:
            try:
                partner.unlink()
            except Exception:
                pass
