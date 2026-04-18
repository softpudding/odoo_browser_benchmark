"""Cleanup for stock.adjust_inventory_with_location_filter."""


PRODUCT_NAME = "Bench Multi Loc Product"
SHELF_A_COMPLETE = "WH/Stock/Shelf A"
SHELF_B_COMPLETE = "WH/Stock/Shelf B"


def cleanup(env):
    product = env["product.product"].search([("name", "=", PRODUCT_NAME)])
    if product:
        env["stock.quant"].search([("product_id", "in", product.ids)]).unlink()
        env["product.template"].search([("name", "=", PRODUCT_NAME)]).unlink()

    for complete in (SHELF_A_COMPLETE, SHELF_B_COMPLETE):
        loc = env["stock.location"].search(
            [("complete_name", "=", complete)], limit=1
        )
        if loc:
            # Only delete if nothing else is using the location.
            other_quants = env["stock.quant"].search_count([
                ("location_id", "=", loc.id),
            ])
            other_moves = env["stock.move"].search_count([
                "|",
                ("location_id", "=", loc.id),
                ("location_dest_id", "=", loc.id),
            ])
            if other_quants == 0 and other_moves == 0:
                try:
                    loc.unlink()
                except Exception:
                    # If unlink fails (e.g., protected system location), just
                    # archive it to keep cleanup idempotent.
                    try:
                        loc.active = False
                    except Exception:
                        pass
