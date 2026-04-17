"""Seed data for fleet.create_vehicle_assign_driver_contract."""


def setup(env):
    contracts = env["fleet.vehicle.log.contract"].search([("ins_ref", "=", "LEASE-2048")])
    contracts.unlink()

    vehicles = env["fleet.vehicle"].search([("license_plate", "=", "FSM-2048")])
    vehicles.unlink()

    partner = env["res.partner"].search([("name", "=", "Avery Collins")], limit=1)
    if not partner:
        partner = env["res.partner"].create({"name": "Avery Collins"})

    vendor = env["res.partner"].search([("name", "=", "Northwind Leasing")], limit=1)
    if not vendor:
        vendor = env["res.partner"].create({
            "name": "Northwind Leasing",
            "supplier_rank": 1,
        })

    brand = env["fleet.vehicle.model.brand"].search([("name", "=", "Zephyr")], limit=1)
    if not brand:
        brand = env["fleet.vehicle.model.brand"].create({"name": "Zephyr"})

    model = env["fleet.vehicle.model"].search([("name", "=", "Cargo EV")], limit=1)
    if not model:
        model = env["fleet.vehicle.model"].create({
            "name": "Cargo EV",
            "brand_id": brand.id,
        })
