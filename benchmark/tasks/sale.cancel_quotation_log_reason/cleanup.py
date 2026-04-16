"""Clean up artifacts from previous runs."""


def cleanup(env):
    refs = ["BENCH-CANCEL-01", "BENCH-NOCANCEL-A", "BENCH-NOCANCEL-B"]
    orders = env["sale.order"].search([("client_order_ref", "in", refs)])
    for so in orders:
        env["mail.message"].search([
            ("model", "=", "sale.order"),
            ("res_id", "=", so.id),
            ("subtype_id.name", "=", "Note"),
        ]).unlink()
        if so.state == "sale":
            so.action_cancel()
        so.unlink()
