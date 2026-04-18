"""Seed for stock.count_inventory_apply_with_date.

Creates a single storable product 'Bench Stock Counter' with an existing
on-hand quantity of 10 at WH/Stock. The agent must use the Physical Inventory
view to update the counted quantity to 25, set the inventory date to
2026-03-20, and apply the adjustment from the row-level Apply button.
"""


PRODUCT_NAME = "Bench Stock Counter"


def setup(env):
    # --- Cleanup prior runs ---
    existing = env["product.product"].search([("name", "=", PRODUCT_NAME)])
    if existing:
        env["stock.quant"].search([("product_id", "in", existing.ids)]).unlink()
        env["product.template"].search([("name", "=", PRODUCT_NAME)]).unlink()

    # --- Locate WH/Stock ---
    stock_loc = env["stock.location"].search(
        [("complete_name", "=", "WH/Stock")], limit=1
    )
    if not stock_loc:
        stock_loc = env["stock.location"].search(
            [("name", "=", "Stock"), ("usage", "=", "internal")], limit=1
        )
    if not stock_loc:
        raise RuntimeError("Cannot find WH/Stock location")

    # --- Create the storable product ---
    tmpl = env["product.template"].create({
        "name": PRODUCT_NAME,
        "type": "consu",
        "is_storable": True,  # Odoo 19: storable = consu + is_storable=True
        "sale_ok": False,
        "purchase_ok": False,
        "list_price": 15.0,
    })
    product = tmpl.product_variant_id

    # --- Seed an on-hand quantity of 10 at WH/Stock ---
    quant = env["stock.quant"].with_context(inventory_mode=True).create([{
        "product_id": product.id,
        "location_id": stock_loc.id,
        "inventory_quantity": 10.0,
    }])
    quant.action_apply_inventory()

    env.cr.execute("SELECT 1")  # force flush
