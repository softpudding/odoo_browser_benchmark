"""Cleanup for stock.create_putaway_rule_for_product."""


PRODUCT_NAME = "Bench Putaway Product"
SUBLOCATION_NAME = "Bench Shelf A"
SUBLOCATION_COMPLETE = "WH/Stock/Bench Shelf A"


def cleanup(env):
    # Drop any putaway rules referencing the seeded product or sub-location.
    products = env["product.product"].search([("name", "=", PRODUCT_NAME)])
    if products:
        env["stock.putaway.rule"].search(
            [("product_id", "in", products.ids)]
        ).unlink()

    sub = env["stock.location"].search(
        [("complete_name", "=", SUBLOCATION_COMPLETE)], limit=1
    )
    if not sub:
        sub = env["stock.location"].search(
            [("name", "=", SUBLOCATION_NAME)], limit=1
        )
    if sub:
        env["stock.putaway.rule"].search(
            ["|",
             ("location_in_id", "in", sub.ids),
             ("location_out_id", "in", sub.ids)]
        ).unlink()
        env["stock.quant"].search(
            [("location_id", "in", sub.ids)]
        ).unlink()
        other_moves = env["stock.move"].search_count([
            "|",
            ("location_id", "in", sub.ids),
            ("location_dest_id", "in", sub.ids),
        ])
        if other_moves == 0:
            try:
                sub.unlink()
            except Exception:
                try:
                    sub.active = False
                except Exception:
                    pass
        else:
            try:
                sub.active = False
            except Exception:
                pass

    if products:
        env["stock.quant"].search(
            [("product_id", "in", products.ids)]
        ).unlink()
        try:
            env["product.template"].search(
                [("name", "=", PRODUCT_NAME)]
            ).unlink()
        except Exception:
            pass
