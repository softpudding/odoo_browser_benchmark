"""Postcondition checks for mrp.convert_bom_to_kit_type."""


def check(env):
    failures = []

    prod = env["product.product"].search([
        ("name", "=", "Benchmark Modular Shelving"),
    ], limit=1)
    if not prod:
        return ["Product 'Benchmark Modular Shelving' not found"]

    bom = env["mrp.bom"].search([
        ("product_tmpl_id", "=", prod.product_tmpl_id.id),
    ], limit=1)
    if not bom:
        return ["BOM for 'Benchmark Modular Shelving' not found"]

    if bom.type != "phantom":
        failures.append(f"BOM type is '{bom.type}', expected 'phantom' (Kit)")

    if bom.product_qty != 1.0:
        failures.append(f"BOM product_qty changed to {bom.product_qty}, expected 1.0")

    if len(bom.bom_line_ids) != 3:
        failures.append(
            f"BOM has {len(bom.bom_line_ids)} components, expected 3 (components must not be modified)"
        )

    return failures
