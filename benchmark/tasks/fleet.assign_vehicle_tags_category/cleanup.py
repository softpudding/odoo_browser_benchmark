"""Cleanup for fleet.assign_vehicle_tags_category."""


PLATE = "TAG-001"
MODEL_NAME = "Benchmark Tag Vehicle"
TAG_NAMES = ["Executive", "Sales Team", "Reserve"]
CATEGORY_NAMES = ["Company Cars", "Pool Cars"]


def cleanup(env):
    vehicles = env["fleet.vehicle"].search([("license_plate", "=", PLATE)])
    if vehicles:
        vehicles.unlink()

    env["fleet.vehicle.model"].search([("name", "=", MODEL_NAME)]).unlink()
    env["fleet.vehicle.tag"].search([("name", "in", TAG_NAMES)]).unlink()
    env["fleet.vehicle.model.category"].search(
        [("name", "in", CATEGORY_NAMES)]
    ).unlink()
