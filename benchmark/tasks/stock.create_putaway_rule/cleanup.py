"""Cleanup for stock.create_putaway_rule."""

TARGET_PRODUCT = "Storage Box Echo"
DISTRACTOR_PRODUCT = "Storage Box Foxtrot"
SHELF_NAME = "Shelf A1"


def cleanup(env):
    prods = env["product.product"].search([
        ("name", "in", [TARGET_PRODUCT, DISTRACTOR_PRODUCT])
    ])
    if prods:
        env["stock.putaway.rule"].search([
            ("product_id", "in", prods.ids)
        ]).unlink()

    # Also remove any rules routed TO the shelf we created (in case the
    # agent created a rule without a product, via a category).
    shelf = env["stock.location"].search([
        ("name", "=", SHELF_NAME),
        ("complete_name", "=", f"WH/Stock/{SHELF_NAME}"),
    ], limit=1)
    if shelf:
        env["stock.putaway.rule"].search([
            ("location_out_id", "=", shelf.id),
        ]).unlink()
