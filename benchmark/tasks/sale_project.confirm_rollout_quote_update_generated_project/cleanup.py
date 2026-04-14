"""Cleanup for sale_project.confirm_rollout_quote_update_generated_project."""


def cleanup(env):
    orders = env["sale.order"].search([
        ("client_order_ref", "in", ["ROLL-PROJ-31", "ROLL-PROJ-31-LIVE", "ROLL-PROJ-32"]),
    ])
    for order in orders:
        if order.state == "sale":
            order.action_cancel()
        if order.state in ("draft", "cancel"):
            order.unlink()
