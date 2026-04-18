"""Cleanup for inventory.create_storage_category_assign_to_location."""

CATEGORY_NAME = "Cold Chain"
STOCK_COMPLETE = "WH/Stock"


def cleanup(env):
    # Clear storage_category_id on WH/Stock if set
    stock_loc = env["stock.location"].search([
        ("complete_name", "=", STOCK_COMPLETE),
        ("usage", "=", "internal"),
    ], limit=1)
    if stock_loc and stock_loc.storage_category_id:
        stock_loc.write({"storage_category_id": False})

    # Remove any Cold Chain categories
    prior = env["stock.storage.category"].search([
        ("name", "=", CATEGORY_NAME),
    ])
    if prior:
        env["stock.location"].search([
            ("storage_category_id", "in", prior.ids),
        ]).write({"storage_category_id": False})
        prior.unlink()
