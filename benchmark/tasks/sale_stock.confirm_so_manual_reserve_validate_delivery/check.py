"""Postcondition checks for sale_stock.confirm_so_manual_reserve_validate_delivery."""


def check(env):
    failures = []

    so = env["sale.order"].search([("client_order_ref", "=", "BENCH-SO-RESERVE")], limit=1)
    if not so:
        return ["Target SO 'BENCH-SO-RESERVE' not found"]

    if so.state != "sale":
        failures.append(f"SO state is {so.state!r}, expected 'sale'")

    if len(so.picking_ids) != 1:
        failures.append(f"Expected exactly 1 delivery, found {len(so.picking_ids)}")
    else:
        picking = so.picking_ids[0]
        if picking.state != "done":
            failures.append(f"Delivery state is {picking.state!r}, expected 'done'")

    expected = {
        "Bench Servo Housing": 7.0,
        "Bench Control Cable": 5.0,
    }
    for line in so.order_line:
        qty = expected.pop(line.product_id.name, None)
        if qty is None:
            failures.append(f"Unexpected SO line {line.product_id.name!r}")
            continue
        if abs(line.product_uom_qty - qty) > 0.001:
            failures.append(
                f"{line.product_id.name} ordered qty is {line.product_uom_qty}, expected {qty}"
            )
        if abs(line.qty_delivered - qty) > 0.001:
            failures.append(
                f"{line.product_id.name} delivered qty is {line.qty_delivered}, expected {qty}"
            )
    for missing in expected:
        failures.append(f"Missing expected SO line {missing!r}")

    dist = env["sale.order"].search([("client_order_ref", "=", "BENCH-SO-RESERVE-DIST")], limit=1)
    if not dist:
        failures.append("Distractor quotation 'BENCH-SO-RESERVE-DIST' is missing")
    elif dist.state != "draft":
        failures.append(f"Distractor quotation state is {dist.state!r}, expected 'draft'")

    return failures
