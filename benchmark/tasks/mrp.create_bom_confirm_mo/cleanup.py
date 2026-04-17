"""Clean up artifacts from previous runs."""

PRODUCT_NAME = "Bench Assembly Table"


def cleanup(env):
    product = env["product.product"].search(
        [("name", "=", PRODUCT_NAME)], limit=1
    )
    if not product:
        return

    # Delete MOs first
    mos = env["mrp.production"].search([("product_id", "=", product.id)])
    for mo in mos:
        if mo.state not in ("cancel", "draft"):
            try:
                mo.action_cancel()
            except Exception:
                pass
    mos.unlink()

    # Delete BOMs
    boms = env["mrp.bom"].search([
        ("product_tmpl_id", "=", product.product_tmpl_id.id)
    ])
    boms.unlink()
