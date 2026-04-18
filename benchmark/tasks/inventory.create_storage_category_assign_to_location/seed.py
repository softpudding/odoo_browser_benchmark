"""Seed for inventory.create_storage_category_assign_to_location.

Category: deep_ui_interaction (MEDIUM, tier=2).

Pre-state:
  - The 'Storage Locations' (group_stock_multi_locations) feature is DISABLED
    in the base snapshot. The agent must enable it themselves via
    Configuration → Settings before the Storage Categories menu / the
    storage_category_id field on stock.location become visible.
  - There is no 'Cold Chain' storage category, and WH/Stock has
    storage_category_id = False.

Cleans up any prior 'Cold Chain' category and clears storage_category_id on
WH/Stock so re-runs start fresh.
"""

CATEGORY_NAME = "Cold Chain"
STOCK_COMPLETE = "WH/Stock"


def _find_stock_location(env):
    loc = env["stock.location"].search([
        ("complete_name", "=", STOCK_COMPLETE),
        ("usage", "=", "internal"),
    ], limit=1)
    if not loc:
        wh = env["stock.warehouse"].search([], limit=1)
        loc = wh.lot_stock_id
    return loc


def setup(env):
    # 1. Cleanup: remove any prior Cold Chain category (and its capacity rules)
    prior = env["stock.storage.category"].search([
        ("name", "=", CATEGORY_NAME),
    ])
    if prior:
        # Clear references from any locations first
        env["stock.location"].search([
            ("storage_category_id", "in", prior.ids),
        ]).write({"storage_category_id": False})
        prior.unlink()

    # 2. Make sure WH/Stock starts with no storage category
    stock_loc = _find_stock_location(env)
    if stock_loc.storage_category_id:
        stock_loc.write({"storage_category_id": False})

    # 3. Make sure the Storage Locations group is DISABLED for admin so the
    # agent must turn it on themselves. This is the explicit prerequisite.
    multi_loc_group = env.ref("stock.group_stock_multi_locations")
    admin = env.ref("base.user_admin")
    # Remove from admin
    if multi_loc_group in admin.group_ids:
        admin.write({"group_ids": [(3, multi_loc_group.id)]})
    # Also remove from the implied portal-user group via the standard pattern
    # (group_stock_multi_locations has no users by default; we just ensure
    # the implied_ids on user-related groups don't keep it on).
    base_user = env.ref("base.group_user")
    if multi_loc_group in base_user.implied_ids:
        base_user.write({"implied_ids": [(3, multi_loc_group.id)]})

    env.cr.execute("SELECT 1")  # force flush
