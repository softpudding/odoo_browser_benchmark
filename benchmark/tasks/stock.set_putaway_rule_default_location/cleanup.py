"""Cleanup for stock.set_putaway_rule_default_location."""

PRODUCT_NAME = "Bench Putaway Item"
SHELF_NAME = "Shelf B"


def cleanup(env):
    # Remove all putaway rules that touch the seeded artifacts.
    prod = env["product.product"].search(
        [("name", "=", PRODUCT_NAME)], limit=1
    )
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

    if prod:
        try:
            env["stock.move.line"].search(
                [("product_id", "=", prod.id)]
            ).sudo().unlink()
        except Exception:
            pass
        try:
            env["stock.move"].search(
                [("product_id", "=", prod.id)]
            ).sudo().unlink()
        except Exception:
            pass
        try:
            env["stock.quant"].with_context(inventory_mode=True).search(
                [("product_id", "=", prod.id)]
            ).sudo().unlink()
        except Exception:
            pass
        try:
            prod.product_tmpl_id.sudo().unlink()
        except Exception:
            pass
