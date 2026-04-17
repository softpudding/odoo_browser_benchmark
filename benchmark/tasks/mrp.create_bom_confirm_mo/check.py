"""Postcondition checks for mrp.create_bom_confirm_mo.

Validates:
1. A BOM exists for "Bench Assembly Table" with 3 components.
2. Components match expected names and quantities.
3. A confirmed MO exists for the same product with qty 10.
"""

PRODUCT_NAME = "Bench Assembly Table"
EXPECTED_COMPONENTS = {
    "Table Leg": 4.0,
    "Table Top Panel": 1.0,
    "Assembly Screw Pack": 2.0,
}


def check(env):
    failures = []

    # Check BOM
    product = env["product.product"].search(
        [("name", "=", PRODUCT_NAME)], limit=1
    )
    if not product:
        return [f"Product '{PRODUCT_NAME}' not found"]

    bom = env["mrp.bom"].search(
        [("product_tmpl_id", "=", product.product_tmpl_id.id)], limit=1
    )
    if not bom:
        return [f"No BOM found for '{PRODUCT_NAME}'"]

    if len(bom.bom_line_ids) != 3:
        failures.append(
            f"BOM has {len(bom.bom_line_ids)} component lines, expected 3"
        )

    for line in bom.bom_line_ids:
        comp_name = line.product_id.name
        if comp_name in EXPECTED_COMPONENTS:
            expected_qty = EXPECTED_COMPONENTS[comp_name]
            if abs(line.product_qty - expected_qty) > 0.01:
                failures.append(
                    f"Component '{comp_name}' qty is {line.product_qty}, "
                    f"expected {expected_qty}"
                )
        else:
            failures.append(f"Unexpected component '{comp_name}' in BOM")

    for comp_name in EXPECTED_COMPONENTS:
        if not bom.bom_line_ids.filtered(
            lambda l, n=comp_name: l.product_id.name == n
        ):
            failures.append(f"Missing component '{comp_name}' in BOM")

    # Check Manufacturing Order
    mo = env["mrp.production"].search(
        [("product_id", "=", product.id)], limit=1
    )
    if not mo:
        failures.append(f"No Manufacturing Order found for '{PRODUCT_NAME}'")
    else:
        if mo.state != "confirmed":
            failures.append(
                f"MO state is '{mo.state}', expected 'confirmed'"
            )
        if abs(mo.product_qty - 10.0) > 0.01:
            failures.append(
                f"MO quantity is {mo.product_qty}, expected 10.0"
            )
        if not mo.bom_id:
            failures.append("MO has no BOM linked")

    return failures
