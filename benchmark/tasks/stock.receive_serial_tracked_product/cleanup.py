"""Cleanup for stock.receive_serial_tracked_product.

Reverses whatever the seed + agent did, so the task can be re-run
idempotently:

- Cancel + unlink the seeded receipt (by origin).
- Drop stock.move.line / stock.move / stock.lot / stock.quant rows
  bound to the seeded product.
- Drop the product template itself.
- Drop any stale lots named SN-BENCH-00X that may have been
  orphaned.
"""

PRODUCT_NAME = "Bench Serial Gadget"
RECEIPT_ORIGIN = "BENCH-SN-RCV-01"
SERIAL_NAMES = ("SN-BENCH-001", "SN-BENCH-002", "SN-BENCH-003")


def cleanup(env):
    # 1. Pickings seeded by this task.
    for pick in env["stock.picking"].search([("origin", "=", RECEIPT_ORIGIN)]):
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
            pick.unlink()
        except Exception:
            pass

    # 2. Cascade-delete move/move_line/lot/quant for the product.
    prods = env["product.product"].search([("name", "=", PRODUCT_NAME)])
    if prods:
        env["stock.move.line"].search([("product_id", "in", prods.ids)]).unlink()
        env["stock.move"].search([("product_id", "in", prods.ids)]).unlink()
        env["stock.quant"].search([("product_id", "in", prods.ids)]).unlink()
        env["stock.lot"].search([("product_id", "in", prods.ids)]).unlink()
        try:
            prods.mapped("product_tmpl_id").unlink()
        except Exception:
            pass

    # 3. Drop any remaining lots with our seed names (orphans).
    stale_lots = env["stock.lot"].search(
        [("name", "in", list(SERIAL_NAMES))]
    )
    if stale_lots:
        try:
            stale_lots.unlink()
        except Exception:
            pass
