"""Seed incorrect on-hand quantities for Physical Inventory task.

Category 5: Deep UI interaction.
The Physical Inventory view uses inline tree editing — the agent must
click directly into quantity cells in a list view and type exact values
for three specific products while leaving two distractor products unchanged.
Browser-use typically fails to interact reliably with inline editable cells
in list/tree views.
"""


def setup(env):
    # Find WH/Stock location
    location = env["stock.location"].search(
        [("complete_name", "=", "WH/Stock")], limit=1
    )
    if not location:
        # Fallback: find any internal stock location named Stock
        location = env["stock.location"].search(
            [("name", "=", "Stock"), ("usage", "=", "internal")], limit=1
        )
    if not location:
        raise ValueError("Cannot find WH/Stock location — is the stock module configured?")

    # Product definitions: (name, type, seeded_wrong_qty, uom_name)
    products_to_adjust = [
        ("Steel Bracket 12\"", 22.0),
        ("Copper Wire 100m", 98.0),
        ("Safety Harness XL", 3.0),
    ]
    distractor_products = [
        ("Latex Work Gloves L", 30.0),
        ("Hard Hat Yellow", 15.0),
    ]
    all_products = products_to_adjust + distractor_products

    # --- Cleanup prior runs: remove existing quants and products ---
    product_names = [p[0] for p in all_products]
    existing_products = env["product.product"].search(
        [("name", "in", product_names)]
    )
    if existing_products:
        # Remove existing quants for these products
        quants = env["stock.quant"].search(
            [("product_id", "in", existing_products.ids), ("location_id", "=", location.id)]
        )
        quants.sudo().unlink()

    # --- Create or find products and set initial on-hand quantities ---
    for name, initial_qty in all_products:
        product = env["product.product"].search([("name", "=", name)], limit=1)
        if not product:
            tmpl = env["product.template"].create({
                "name": name,
                "type": "consu",
                "is_storable": True,  # Odoo 19: storable = consu + is_storable=True
                "list_price": 10.0,
            })
            product = tmpl.product_variant_id
        # Set on-hand quantity via quant (direct write for seed purposes)
        env["stock.quant"]._update_available_quantity(product, location, initial_qty)

    env.cr.execute("SELECT 1")  # force flush
