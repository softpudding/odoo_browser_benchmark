"""Seed for stock.set_storage_category_capacity.

Category: deep_ui_interaction (MEDIUM).

Prepares:
- Enables the Storage Locations feature (stock.group_stock_multi_locations)
  for the admin user so the Storage Categories menu and location
  storage_category_id field become visible in the UI.
- Cleans up any 'Bench Small Bin' storage category and
  'Bench Small Bin Area' location left over from a prior run.
- Creates a fresh internal sub-location WH/Stock/Bench Small Bin Area with
  no storage category assigned.

The agent must then create the storage category and assign it to the
sub-location.
"""


LOCATION_NAME = "Bench Small Bin Area"
CATEGORY_NAME = "Bench Small Bin"


def _get_stock_parent(env):
    loc = env["stock.location"].search(
        [("complete_name", "=", "WH/Stock"), ("usage", "=", "internal")],
        limit=1,
    )
    if not loc:
        loc = env["stock.location"].search(
            [("name", "=", "Stock"), ("usage", "=", "internal")], limit=1
        )
    if not loc:
        wh = env["stock.warehouse"].search([], limit=1)
        if not wh:
            raise RuntimeError("No warehouse found to attach the sub-location")
        loc = wh.lot_stock_id
    return loc


def setup(env):
    # --- Enable Storage Locations (multi-locations) feature ---
    # This surfaces both the Storage Categories menu under Configuration >
    # Warehouse and the Storage Category field on internal stock.location
    # records.
    multi_loc_grp = env.ref(
        "stock.group_stock_multi_locations", raise_if_not_found=False
    )
    if multi_loc_grp:
        # Grant to the admin user so the UI surfaces the feature.
        admin = env.ref("base.user_admin")
        if multi_loc_grp not in admin.group_ids:
            admin.group_ids = [(4, multi_loc_grp.id)]
        # Also grant to the portal-employee base group so the feature is
        # broadly available (mirrors res.config.settings toggling behaviour).
        base_user = env.ref("base.group_user", raise_if_not_found=False)
        if base_user and multi_loc_grp not in base_user.implied_ids:
            base_user.implied_ids = [(4, multi_loc_grp.id)]

    # --- Cleanup prior runs ---
    # Unassign any leftover storage_category_id referencing the old
    # 'Bench Small Bin' category so the category can be unlinked cleanly.
    old_cat = env["stock.storage.category"].search(
        [("name", "=", CATEGORY_NAME)]
    )
    if old_cat:
        env["stock.location"].search(
            [("storage_category_id", "in", old_cat.ids)]
        ).write({"storage_category_id": False})
        old_cat.unlink()

    # Remove any leftover sub-location with the same name.
    old_loc = env["stock.location"].search([("name", "=", LOCATION_NAME)])
    if old_loc:
        # Clear any quants/moves referencing it, archive if unlink fails.
        env["stock.quant"].search(
            [("location_id", "in", old_loc.ids)]
        ).unlink()
        try:
            old_loc.unlink()
        except Exception:
            old_loc.write({"active": False})

    # --- Create the target sub-location under WH/Stock ---
    parent = _get_stock_parent(env)
    env["stock.location"].create({
        "name": LOCATION_NAME,
        "location_id": parent.id,
        "usage": "internal",
    })

    # Sanity check: the sub-location exists with complete_name
    # "WH/Stock/Bench Small Bin Area" and no storage category yet.
    target = env["stock.location"].search(
        [("complete_name", "=", f"WH/Stock/{LOCATION_NAME}")], limit=1
    )
    assert target, (
        f"Seed failed: could not locate the freshly created "
        f"WH/Stock/{LOCATION_NAME} location"
    )
    assert not target.storage_category_id, (
        "Seed failed: the sub-location should not have a storage category "
        "assigned yet"
    )

    # Sanity: no storage category named CATEGORY_NAME should exist now.
    assert not env["stock.storage.category"].search(
        [("name", "=", CATEGORY_NAME)]
    ), f"Seed failed: leftover '{CATEGORY_NAME}' storage category still exists"
