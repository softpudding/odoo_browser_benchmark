"""Cleanup for stock.transfer_create_internal_transfer_validate."""

PRODUCT_NAME = "Bench Move Item"
SHELF_NAME = "Shelf C"
SHELF_COMPLETE = "WH/Stock/Shelf C"


def cleanup(env):
    prod = env["product.product"].search(
        [("name", "=", PRODUCT_NAME)], limit=1
    )
    shelf = env["stock.location"].search([
        ("name", "=", SHELF_NAME),
        ("complete_name", "=", SHELF_COMPLETE),
    ], limit=1)

    # 1. Pickings related to the product or the shelf destination.
    domain = []
    if prod:
        domain = [("move_ids.product_id", "=", prod.id)]
    if shelf:
        if domain:
            domain = ["|", ("location_dest_id", "=", shelf.id)] + domain
        else:
            domain = [("location_dest_id", "=", shelf.id)]
    if domain:
        pickings = env["stock.picking"].search(domain)
        ordered = sorted(
            pickings, key=lambda p: 0 if p.backorder_id else 1
        )
        for pick in ordered:
            if pick.state not in ("done", "cancel"):
                try:
                    pick.action_cancel()
                except Exception:
                    pass
            try:
                pick.move_ids.write({"state": "cancel"})
            except Exception:
                pass
            try:
                pick.write({"state": "cancel"})
            except Exception:
                pass
            try:
                pick.unlink()
            except Exception:
                pass

    # 2. Stale lines / moves / quants on the product.
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
