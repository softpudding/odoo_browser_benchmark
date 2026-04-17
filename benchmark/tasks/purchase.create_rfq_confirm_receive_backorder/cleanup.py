"""Clean up artifacts from previous runs."""


def cleanup(env):
    # Find POs with our vendor reference
    pos = env["purchase.order"].search([
        ("partner_ref", "=", "SRC-PO-2026-Q2"),
    ])
    for po in pos:
        # Remove associated pickings first
        pickings = env["stock.picking"].search([
            ("origin", "=", po.name),
        ])
        for pk in pickings:
            if pk.state not in ("cancel", "done"):
                pk.action_cancel()
            pk.unlink()
        if po.state in ("purchase", "done"):
            po.button_cancel()
        po.unlink()

    # Clean up products created for this task
    for name in [
        "Hydraulic Cylinder 50mm",
        "Pressure Gauge PSI",
        "Flow Control Valve",
    ]:
        product = env["product.product"].search(
            [("name", "=", name)], limit=1
        )
        if product:
            tmpl = product.product_tmpl_id
            product.unlink()
            if tmpl.exists():
                tmpl.unlink()

    # Clean up vendor
    partner = env["res.partner"].search(
        [("name", "=", "Summit Ridge Components")], limit=1
    )
    if partner:
        partner.unlink()
