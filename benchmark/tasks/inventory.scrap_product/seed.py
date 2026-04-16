"""Seed a product with on-hand quantity for the scrap task.

Category: deep_ui_interaction (EASY).
Starting state: Product "Steel Bracket 12" with on-hand quantity of 50 units.
The agent must use the Scrap wizard to scrap 5 units.
"""


def setup(env):
    # --- Cleanup prior runs ---
    env["stock.scrap"].search([("product_id.name", "=", "Steel Bracket 12")]).unlink()

    # --- Ensure product exists ---
    product = env["product.product"].search([("name", "=", "Steel Bracket 12")], limit=1)
    if not product:
        tmpl = env["product.template"].create({
            "name": "Steel Bracket 12\"",
            "type": "product",
            "list_price": 25.0,
        })
        product = tmpl.product_variant_id

    # --- Ensure a warehouse location exists ---
    location = env["stock.location"].search([("usage", "=", "internal")], limit=1)
    if not location:
        warehouse = env["stock.warehouse"].search([], limit=1)
        if warehouse:
            location = warehouse.lot_stock_id

    # --- Set on-hand quantity to 50 ---
    if location:
        env["stock.quant"].create({
            "product_id": product.id,
            "location_id": location.id,
            "quantity": 50.0,
        })