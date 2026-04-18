"""Postcondition checks for stock.package_products_validate_delivery."""


def check(env):
    failures = []

    picking = env["stock.picking"].search([("origin", "=", "BENCH-PACK-DEL-01")], limit=1)
    if not picking:
        return ["Delivery 'BENCH-PACK-DEL-01' not found"]

    if picking.state != "done":
        failures.append(f"Delivery state is '{picking.state}', expected 'done'")

    packages = picking.move_line_ids.mapped("result_package_id")
    if not packages:
        failures.append("No destination package was assigned to the delivery lines")
    elif len(packages) != 1:
        failures.append(f"Expected exactly 1 destination package, found {len(packages)}")

    for line in picking.move_line_ids:
        if not line.result_package_id:
            failures.append(f"Move line for '{line.product_id.display_name}' was not packaged")
        if abs(line.quantity - line.move_id.product_uom_qty) > 0.0001:
            failures.append(
                f"Move line for '{line.product_id.display_name}' has quantity {line.quantity}, expected {line.move_id.product_uom_qty}"
            )

    distractor = env["stock.picking"].search([("origin", "=", "BENCH-PACK-DEL-OTHER")], limit=1)
    if distractor and distractor.state == "done":
        failures.append("Distractor delivery was incorrectly validated")

    return failures
