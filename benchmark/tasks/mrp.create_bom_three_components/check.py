"""Postcondition checks for mrp.create_bom_three_components."""


PRODUCT_NAME = "Wooden Chair"
EXPECTED_LINES = {
    "Wooden Leg": 4.0,
    "Seat Board": 1.0,
    "Backrest Panel": 1.0,
}


def check(env):
    failures = []

    product = env["product.template"].search([("name", "=", PRODUCT_NAME)])
    if len(product) != 1:
        return [f"Expected exactly 1 product named '{PRODUCT_NAME}', found {len(product)}"]

    boms = env["mrp.bom"].search([("product_tmpl_id", "=", product.id)])
    if len(boms) != 1:
        return [f"Expected exactly 1 BOM for '{PRODUCT_NAME}', found {len(boms)}"]

    bom = boms[0]
    if bom.product_qty != 1.0:
        failures.append(f"BOM product_qty is {bom.product_qty}, expected 1.0")

    if len(bom.bom_line_ids) != 3:
        failures.append(
            f"BOM has {len(bom.bom_line_ids)} component lines, expected exactly 3"
        )

    line_map = {line.product_id.display_name: line.product_qty for line in bom.bom_line_ids}
    if line_map != EXPECTED_LINES:
        failures.append(f"BOM components are {line_map}, expected {EXPECTED_LINES}")

    return failures
