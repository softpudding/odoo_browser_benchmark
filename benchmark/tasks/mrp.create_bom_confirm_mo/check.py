"""Postcondition checks for mrp.create_bom_confirm_mo."""


PRODUCT_NAME = "BenchMaster Assembly Kit"
EXPECTED_CODE = "BM-KIT-26"
EXPECTED_LINES = {
    "BenchMaster Frame": 2.0,
    "BenchMaster Panel": 4.0,
    "BenchMaster Fastener Pack": 1.0,
}


def check(env):
    failures = []

    product = env["product.template"].search([("name", "=", PRODUCT_NAME)])
    if len(product) != 1:
        return [f"Expected exactly 1 product named '{PRODUCT_NAME}', found {len(product)}"]

    boms = env["mrp.bom"].search([
        ("product_tmpl_id", "=", product.id),
        ("code", "=", EXPECTED_CODE),
    ])
    if len(boms) != 1:
        return [f"Expected exactly 1 BOM with code '{EXPECTED_CODE}', found {len(boms)}"]

    bom = boms[0]
    line_map = {line.product_id.display_name: line.product_qty for line in bom.bom_line_ids}
    if line_map != EXPECTED_LINES:
        failures.append(f"BOM lines are {line_map}, expected {EXPECTED_LINES}")

    productions = env["mrp.production"].search([
        ("product_id", "=", product.product_variant_id.id),
        ("product_qty", "=", 10.0),
    ])
    if len(productions) != 1:
        failures.append(f"Expected exactly 1 manufacturing order for 10 units, found {len(productions)}")
        return failures

    production = productions[0]
    if production.state != "confirmed":
        failures.append(f"Manufacturing order state is '{production.state}', expected 'confirmed'")
    if production.bom_id != bom:
        failures.append("Manufacturing order is not linked to the created BOM")

    raw_moves = {move.product_id.display_name: move.product_uom_qty for move in production.move_raw_ids}
    expected_raw_moves = {
        "BenchMaster Frame": 20.0,
        "BenchMaster Panel": 40.0,
        "BenchMaster Fastener Pack": 10.0,
    }
    if raw_moves != expected_raw_moves:
        failures.append(f"Raw material moves are {raw_moves}, expected {expected_raw_moves}")

    return failures
