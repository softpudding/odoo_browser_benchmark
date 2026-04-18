"""Cleanup for stock.create_putaway_rule_for_specific_category."""

CATEGORY_NAME = "Bench Cold Items"
PRODUCT_NAME = "Bench Frozen Salmon"
SHELF_NAME = "Refrigerator"


def cleanup(env):
    cat = env["product.category"].search([("name", "=", CATEGORY_NAME)], limit=1)
    if cat:
        env["stock.putaway.rule"].search([
            ("category_id", "=", cat.id)
        ]).unlink()
    prod = env["product.product"].search([("name", "=", PRODUCT_NAME)], limit=1)
    if prod:
        env["stock.putaway.rule"].search([
            ("product_id", "=", prod.id)
        ]).unlink()
    shelf = env["stock.location"].search([
        ("name", "=", SHELF_NAME),
        ("complete_name", "=", f"WH/Stock/{SHELF_NAME}"),
    ], limit=1)
    if shelf:
        env["stock.putaway.rule"].search([
            ("location_out_id", "=", shelf.id),
        ]).unlink()
