"""Clean up artifacts from previous runs."""


def cleanup(env):
    product_names = [
        "Steel Bracket 12\"",
        "Copper Wire 100m",
        "Safety Harness XL",
        "Latex Work Gloves L",
        "Hard Hat Yellow",
    ]
    location = env["stock.location"].search(
        [("complete_name", "=", "WH/Stock")], limit=1
    )
    if not location:
        location = env["stock.location"].search(
            [("name", "=", "Stock"), ("usage", "=", "internal")], limit=1
        )
    products = env["product.product"].search([("name", "in", product_names)])
    if products and location:
        quants = env["stock.quant"].search([
            ("product_id", "in", products.ids),
            ("location_id", "=", location.id),
        ])
        quants.sudo().unlink()
    products.unlink()
