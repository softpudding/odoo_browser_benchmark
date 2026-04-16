"""Cleanup for stock.update_reorder_rule."""

TARGET_PRODUCT = "Steel Bracket 12\""
DISTRACTOR_PRODUCT = "Copper Wire 100m"


def cleanup(env):
    products = env["product.product"].search([
        ("name", "in", [TARGET_PRODUCT, DISTRACTOR_PRODUCT])
    ])
    if products:
        env["stock.warehouse.orderpoint"].search([
            ("product_id", "in", products.ids)
        ]).unlink()
