"""Cleanup for stock.scrap_product_from_receipt."""

PRODUCT_NAME = "Bench Scrap Product"
RECEIPT_REF = "BENCH-RCV-SCRAP-01"


def cleanup(env):
    # Delete scraps first (they may block picking deletion via stock moves)
    env["stock.scrap"].search([
        ("product_id.display_name", "=", PRODUCT_NAME),
    ]).sudo().unlink()

    picks = env["stock.picking"].search([("origin", "=", RECEIPT_REF)])
    for pick in picks:
        try:
            if pick.state != "done":
                pick.action_cancel()
            pick.unlink()
        except Exception:
            try:
                pick.sudo().unlink()
            except Exception:
                pass

    env["stock.move.line"].search([
        ("product_id.display_name", "=", PRODUCT_NAME),
        ("state", "!=", "done"),
    ]).unlink()
    env["product.template"].search([("name", "=", PRODUCT_NAME)]).unlink()
