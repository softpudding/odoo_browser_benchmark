"""Cleanup for stock.count_inventory_apply_with_date."""


PRODUCT_NAME = "Bench Stock Counter"


def cleanup(env):
    product = env["product.product"].search([("name", "=", PRODUCT_NAME)])
    if product:
        env["stock.quant"].search([("product_id", "in", product.ids)]).unlink()
        env["product.template"].search([("name", "=", PRODUCT_NAME)]).unlink()
