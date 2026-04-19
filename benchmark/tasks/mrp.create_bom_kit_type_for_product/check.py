"""Postcondition checks for mrp.create_bom_kit_type_for_product.

Validates that:
1. Exactly one mrp.bom exists for product 'Bench Kit Finished'.
2. Its `type` is 'phantom' (UI label 'Kit') — NOT 'normal' (the default
   'Manufacture this Product').
3. product_qty == 1.0.
4. Exactly 2 bom_line_ids:
   - Bench Kit Comp A @ qty 2.0
   - Bench Kit Comp B @ qty 3.0
5. No extra / duplicate BoM lines.
"""


FINISHED_NAME = "Bench Kit Finished"
EXPECTED_LINES = {
    "Bench Kit Comp A": 2.0,
    "Bench Kit Comp B": 3.0,
}


def check(env):
    failures = []

    product = env["product.template"].search([("name", "=", FINISHED_NAME)])
    if len(product) != 1:
        return [
            f"Expected exactly 1 product.template named {FINISHED_NAME!r}, "
            f"found {len(product)}"
        ]

    boms = env["mrp.bom"].search([("product_tmpl_id", "=", product.id)])
    if len(boms) != 1:
        return [
            f"Expected exactly 1 mrp.bom for {FINISHED_NAME!r}, "
            f"found {len(boms)}"
        ]

    bom = boms[0]

    # --- Type must be 'phantom' (UI label 'Kit') ---
    if bom.type != "phantom":
        failures.append(
            f"BoM type is {bom.type!r}, expected 'phantom' (UI label 'Kit'). "
            f"The default 'Manufacture this Product' option stores type='normal' "
            f"and is not a kit BoM."
        )

    if abs((bom.product_qty or 0.0) - 1.0) > 1e-6:
        failures.append(
            f"BoM product_qty is {bom.product_qty}, expected 1.0"
        )

    # --- Exactly 2 component lines ---
    if len(bom.bom_line_ids) != 2:
        failures.append(
            f"BoM has {len(bom.bom_line_ids)} component lines "
            f"(products: {bom.bom_line_ids.mapped('product_id.display_name')}), "
            f"expected exactly 2"
        )
        return failures

    line_map = {
        line.product_id.display_name: line.product_qty
        for line in bom.bom_line_ids
    }

    for comp_name, expected_qty in EXPECTED_LINES.items():
        actual = line_map.get(comp_name)
        if actual is None:
            failures.append(
                f"Expected component {comp_name!r} missing from bom_line_ids "
                f"(present: {sorted(line_map.keys())})"
            )
            continue
        if abs(actual - expected_qty) > 1e-6:
            failures.append(
                f"Component {comp_name!r} has product_qty={actual}, "
                f"expected {expected_qty}"
            )

    extras = set(line_map.keys()) - set(EXPECTED_LINES.keys())
    if extras:
        failures.append(
            f"Unexpected extra BoM components: {sorted(extras)}"
        )

    return failures
