"""Postcondition checks for fleet.create_vehicle_assign_driver_contract."""


def check(env):
    failures = []
    vehicle = env["fleet.vehicle"].search([("license_plate", "=", "FSM-2048")], limit=1)
    if not vehicle:
        return ["Vehicle FSM-2048 not found"]
    if vehicle.model_id.name != "Cargo EV":
        failures.append(f"Vehicle model is {vehicle.model_id.name!r}")
    if vehicle.driver_id.name != "Avery Collins":
        failures.append(f"Vehicle driver is {vehicle.driver_id.name!r}")
    if str(vehicle.acquisition_date) != "2026-04-12":
        failures.append(f"Registration date is {vehicle.acquisition_date!s}")

    contract = env["fleet.vehicle.log.contract"].search([("ins_ref", "=", "LEASE-2048")], limit=1)
    if not contract:
        failures.append("Contract LEASE-2048 not found")
        return failures
    if contract.vehicle_id != vehicle:
        failures.append("Contract is not linked to the created vehicle")
    if contract.insurer_id.name != "Northwind Leasing":
        failures.append(f"Contract vendor is {contract.insurer_id.name!r}")
    if str(contract.start_date) != "2026-04-15":
        failures.append(f"Contract start date is {contract.start_date!s}")
    if str(contract.expiration_date) != "2026-10-15":
        failures.append(f"Contract expiration date is {contract.expiration_date!s}")
    return failures
