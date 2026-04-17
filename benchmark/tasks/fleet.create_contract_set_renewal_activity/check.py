"""Postcondition checks for fleet.create_contract_set_renewal_activity."""


def check(env):
    failures = []
    vehicle = env["fleet.vehicle"].search([("license_plate", "=", "FLE-6124")], limit=1)
    if not vehicle:
        return ["Vehicle FLE-6124 not found"]
    if vehicle.model_id.name != "Cargo EV":
        failures.append(f"Vehicle model is {vehicle.model_id.name!r}")
    if vehicle.driver_id.name != "Avery Collins":
        failures.append(f"Vehicle driver is {vehicle.driver_id.name!r}")
    if str(vehicle.acquisition_date) != "2026-04-18":
        failures.append(f"Registration date is {vehicle.acquisition_date!s}")

    contract = env["fleet.vehicle.log.contract"].search([("ins_ref", "=", "RENEW-6124")], limit=1)
    if not contract:
        failures.append("Contract RENEW-6124 not found")
        return failures
    if contract.vehicle_id != vehicle:
        failures.append("Contract is not linked to the created vehicle")
    if contract.insurer_id.name != "Northwind Leasing":
        failures.append(f"Contract vendor is {contract.insurer_id.name!r}")
    if str(contract.start_date) != "2026-04-20":
        failures.append(f"Contract start date is {contract.start_date!s}")
    if str(contract.expiration_date) != "2026-11-20":
        failures.append(f"Contract expiration date is {contract.expiration_date!s}")
    if contract.user_id.login != "admin":
        failures.append(f"Contract responsible is {contract.user_id.login!r}, expected 'admin'")

    renewal_activities = contract.activity_ids.filtered(
        lambda act: act.activity_type_id.name == "Contract to Renew"
    )
    if len(renewal_activities) != 1:
        failures.append(
            f"Expected exactly 1 Contract to Renew activity, found {len(renewal_activities)}"
        )
    else:
        activity = renewal_activities[0]
        if str(activity.date_deadline) != "2026-11-20":
            failures.append(f"Renewal activity deadline is {activity.date_deadline!s}")
        if activity.user_id.login != "admin":
            failures.append(f"Renewal activity assigned to {activity.user_id.login!r}")
    return failures
