"""Postcondition checks for mrp.create_bom_with_components."""


PRODUCT_NAME = "Bench Assembled Gadget"
BOM_CODE = "BOM-REFERENCE"
EXPECTED_LINES = {
    "Bench Steel Frame": 1.0,
    "Bench Control Board": 1.0,
    "Bench Power Unit": 2.0,
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

    if (bom.code or "") != BOM_CODE:
        failures.append(f"BOM code is {bom.code!r}, expected {BOM_CODE!r}")

    if len(bom.bom_line_ids) != 3:
        failures.append(
            f"BOM has {len(bom.bom_line_ids)} component lines, expected exactly 3"
        )
        return failures

    line_map = {line.product_id.display_name: line.product_qty for line in bom.bom_line_ids}
    if line_map != EXPECTED_LINES:
        failures.append(f"BOM components are {line_map}, expected {EXPECTED_LINES}")

    for line in bom.bom_line_ids:
        name = line.product_id.display_name
        if name not in EXPECTED_LINES:
            failures.append(f"Unexpected component line: {name}")
            continue
        if line.product_qty != EXPECTED_LINES[name]:
            failures.append(
                f"Component '{name}' qty is {line.product_qty}, expected {EXPECTED_LINES[name]}"
            )

    return failures
