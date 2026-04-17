"""Postcondition checks for mrp.surgical_bom_component_qty_edit."""


FINISHED = "Benchmark Assembly Gamma"
EXPECTED = {
    "Gamma Frame": 1,
    "Gamma Panel": 2,
    "Gamma Bolt M6": 6,  # updated target: 4 -> 6
    "Gamma Cable": 3,
    "Gamma Sticker": 1,
}


def check(env):
    failures = []

    finished = env["product.product"].search([("name", "=", FINISHED)], limit=1)
    if not finished:
        return [f"Finished product '{FINISHED}' not found"]

    boms = env["mrp.bom"].search([
        ("product_tmpl_id", "=", finished.product_tmpl_id.id),
    ])
    if len(boms) != 1:
        failures.append(
            f"Expected exactly 1 BOM for '{FINISHED}', found {len(boms)}"
        )
    if not boms:
        return failures
    bom = boms[0]

    lines_by_name = {
        l.product_id.name: l for l in bom.bom_line_ids
    }

    if len(bom.bom_line_ids) != len(EXPECTED):
        failures.append(
            f"BOM has {len(bom.bom_line_ids)} component lines, "
            f"expected {len(EXPECTED)}"
        )

    for name, want_qty in EXPECTED.items():
        line = lines_by_name.get(name)
        if not line:
            failures.append(f"Component '{name}' missing from BOM")
            continue
        if abs((line.product_qty or 0.0) - want_qty) > 1e-6:
            if name == "Gamma Bolt M6":
                failures.append(
                    f"Target component 'Gamma Bolt M6' quantity is "
                    f"{line.product_qty}, expected 6"
                )
            else:
                failures.append(
                    f"Side-effect: component '{name}' quantity changed to "
                    f"{line.product_qty}, expected {want_qty}"
                )

    return failures
