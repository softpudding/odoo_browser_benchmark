"""Clean up artifacts from previous runs."""


def cleanup(env):
    vendor = env["res.partner"].search(
        [("name", "=", "Pinnacle Hardware")], limit=1
    )
    if not vendor:
        return
    pos = env["purchase.order"].search([
        ("partner_id", "=", vendor.id),
        ("partner_ref", "=", "BENCH-RFQ-UPD"),
    ])
    for po in pos:
        if po.state in ("purchase", "done"):
            po.button_cancel()
        po.unlink()
