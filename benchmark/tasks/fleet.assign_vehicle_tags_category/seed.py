"""Seed data for fleet.assign_vehicle_tags_category.

Creates a single vehicle (Toyota/Benchmark Tag Vehicle/TAG-001) with NO
tags and NO category. Also creates three fleet.vehicle.tag records
("Executive", "Sales Team", "Reserve") and two
fleet.vehicle.model.category records ("Company Cars", "Pool Cars"),
including distractors the agent must NOT pick.

In Odoo 19, the fleet vehicle form uses:
  - tag_ids : Many2many -> fleet.vehicle.tag  (widget: many2many_tags,
    options {'no_create_edit': True} so the agent must pick an existing tag)
  - category_id : Many2one -> fleet.vehicle.model.category
    (computed from the model but store=True readonly=False, so it is
    settable and persisted on the form).
"""


VEHICLE_LABEL = "Benchmark Tag Vehicle"  # fleet.vehicle.model.name
PLATE = "TAG-001"
BRAND_NAME = "Toyota"
MODEL_NAME = VEHICLE_LABEL

TAG_NAMES = ["Executive", "Sales Team"]
DISTRACTOR_TAG = "Reserve"

CATEGORY_NAME = "Company Cars"
DISTRACTOR_CATEGORY = "Pool Cars"


def setup(env):
    Vehicle = env["fleet.vehicle"]
    Brand = env["fleet.vehicle.model.brand"]
    Model = env["fleet.vehicle.model"]
    Tag = env["fleet.vehicle.tag"]
    Category = env["fleet.vehicle.model.category"]

    # --- Cleanup prior runs ---
    stale_vehicles = Vehicle.search([("license_plate", "=", PLATE)])
    if stale_vehicles:
        stale_vehicles.unlink()

    stale_models = Model.search([("name", "=", MODEL_NAME)])
    stale_models.unlink()

    Tag.search([("name", "in", TAG_NAMES + [DISTRACTOR_TAG])]).unlink()
    Category.search([("name", "in", [CATEGORY_NAME, DISTRACTOR_CATEGORY])]).unlink()

    # --- Ensure brand + model exist ---
    brand = Brand.search([("name", "=", BRAND_NAME)], limit=1)
    if not brand:
        brand = Brand.create({"name": BRAND_NAME})

    model = Model.create({
        "name": MODEL_NAME,
        "brand_id": brand.id,
        "vehicle_type": "car",
    })

    # --- Create the two wanted tags + one distractor ---
    for name in TAG_NAMES + [DISTRACTOR_TAG]:
        Tag.create({"name": name})

    # --- Create the wanted category + one distractor ---
    Category.create({"name": CATEGORY_NAME})
    Category.create({"name": DISTRACTOR_CATEGORY})

    # --- Create the vehicle (no tags, no category assigned yet) ---
    # category_id is a computed field with store=True readonly=False that
    # inherits from model_id. We did NOT set a category on the model, so
    # the vehicle's category_id will be empty; the agent must set it.
    admin_partner = env.ref("base.partner_admin", raise_if_not_found=False)
    vals = {
        "license_plate": PLATE,
        "model_id": model.id,
    }
    if admin_partner:
        vals["driver_id"] = admin_partner.id
    Vehicle.create(vals)
