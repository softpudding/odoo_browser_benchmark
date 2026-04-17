"""Postcondition checks for point_of_sale.open_session_sell_product_cash."""


CONFIG_NAME = "Benchmark Counter"
PRODUCT_NAME = "Counter Snack Box"


def check(env):
    failures = []

    orders = env["pos.order"].search([("config_id.name", "=", CONFIG_NAME)])
    if len(orders) != 1:
        return [f"Expected exactly 1 POS order for '{CONFIG_NAME}', found {len(orders)}"]

    order = orders[0]
    lines = order.lines.filtered(lambda line: line.product_id.display_name == PRODUCT_NAME)
    if len(lines) != 1:
        failures.append(f"Expected exactly 1 order line for '{PRODUCT_NAME}', found {len(lines)}")
    else:
        if abs(lines[0].qty - 1.0) > 0.0001:
            failures.append(f"Order quantity is {lines[0].qty}, expected 1.0")

    if order.state not in {"paid", "done", "invoiced"}:
        failures.append(f"POS order state is '{order.state}', expected a paid order state")

    return failures
