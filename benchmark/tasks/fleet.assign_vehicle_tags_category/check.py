"""Postcondition checks for fleet.assign_vehicle_tags_category."""


PLATE = "TAG-001"
REQUIRED_TAGS = {"Executive", "Sales Team"}
CATEGORY_NAME = "Company Cars"
DISTRACTOR_TAG = "Reserve"
DISTRACTOR_CATEGORY = "Pool Cars"


def check(env):
    failures = []

    vehicles = env["fleet.vehicle"].search([("license_plate", "=", PLATE)])
    if len(vehicles) != 1:
        return [
            f"Expected exactly 1 vehicle with plate {PLATE!r}, found {len(vehicles)}"
        ]
    vehicle = vehicles[0]

    tag_names = set(vehicle.tag_ids.mapped("name"))
    missing = REQUIRED_TAGS - tag_names
    if missing:
        failures.append(
            f"Vehicle is missing required tags: {sorted(missing)} "
            f"(currently has: {sorted(tag_names)})"
        )

    if DISTRACTOR_TAG in tag_names:
        failures.append(
            f"Distractor tag {DISTRACTOR_TAG!r} was incorrectly added to the vehicle"
        )

    if not vehicle.category_id:
        failures.append("Vehicle category_id is not set")
    elif vehicle.category_id.name != CATEGORY_NAME:
        failures.append(
            f"Vehicle category is {vehicle.category_id.name!r}, "
            f"expected {CATEGORY_NAME!r}"
        )

    return failures
