"""Clean up artifacts from previous runs."""


def cleanup(env):
    env["mail.message"].search([
        ("subject", "=", "Sterling components order follow-up"),
    ]).unlink()

    pos = env["purchase.order"].search([
        ("partner_ref", "in", ["MED-SEND-PO-01", "MED-SEND-PO-02"]),
    ])
    for po in pos:
        if po.state in ("purchase", "done"):
            po.button_cancel()
        po.unlink()
