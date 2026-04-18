"""Postcondition check for mrp.bom_with_kit_component_confirm_mo.

Validates that:
1. MO 'M-BENCH-KIT-001' exists and is in state 'confirmed'.
2. The finished product is Bench Assembly, qty 1.
3. move_raw_ids contains EXACTLY 3 rows:
   - Bench Sub-A (qty 1)
   - Bench Sub-B (qty 2)
   - Bench Frame (qty 1)
4. No raw move references 'Bench Kit' (phantom expansion must have occurred).
5. No backorder / duplicate MO with the same name prefix.
"""


MO_NAME = "M-BENCH-KIT-001"
ASSEMBLY_NAME = "Bench Assembly"
KIT_NAME = "Bench Kit"

EXPECTED_RAW = {
    "Bench Sub-A": 1.0,
    "Bench Sub-B": 2.0,
    "Bench Frame": 1.0,
}


def check(env):
    failures = []

    mos = env["mrp.production"].search([("name", "=", MO_NAME)])
    if not mos:
        return [f"Manufacturing order {MO_NAME!r} not found"]
    if len(mos) > 1:
        failures.append(
            f"Expected exactly 1 MO named {MO_NAME!r}, found {len(mos)}"
        )
    mo = mos[0]

    if mo.state != "confirmed":
        failures.append(
            f"MO state is {mo.state!r}, expected 'confirmed'"
        )

    if mo.product_id.name != ASSEMBLY_NAME:
        failures.append(
            f"MO product is {mo.product_id.name!r}, expected {ASSEMBLY_NAME!r}"
        )

    if abs(mo.product_qty - 1.0) > 1e-6:
        failures.append(
            f"MO product_qty is {mo.product_qty}, expected 1.0"
        )

    # --- move_raw_ids must show phantom expansion (3 rows, no Bench Kit). ---
    raw_by_name = {}
    for move in mo.move_raw_ids:
        raw_by_name.setdefault(move.product_id.name, 0.0)
        raw_by_name[move.product_id.name] += move.product_uom_qty

    if KIT_NAME in raw_by_name:
        failures.append(
            f"Raw move for {KIT_NAME!r} present — kit BoM did not expand "
            f"(move_raw_ids products: {sorted(raw_by_name.keys())})"
        )

    for comp_name, expected_qty in EXPECTED_RAW.items():
        actual = raw_by_name.get(comp_name)
        if actual is None:
            failures.append(
                f"Expected raw component {comp_name!r} missing from move_raw_ids "
                f"(present: {sorted(raw_by_name.keys())})"
            )
            continue
        if abs(actual - expected_qty) > 1e-6:
            failures.append(
                f"Raw component {comp_name!r} has product_uom_qty={actual}, "
                f"expected {expected_qty}"
            )

    # Exactly these three components — no extras.
    extras = set(raw_by_name.keys()) - set(EXPECTED_RAW.keys())
    if extras:
        failures.append(
            f"Unexpected extra raw components on MO: {sorted(extras)}"
        )

    # There should be exactly 3 move_raw_ids rows (no duplicates / splits).
    if len(mo.move_raw_ids) != 3:
        failures.append(
            f"Expected exactly 3 move_raw_ids rows, found {len(mo.move_raw_ids)} "
            f"(products: {mo.move_raw_ids.mapped('product_id.name')})"
        )

    # No backorder MO with the same prefix.
    backorders = env["mrp.production"].search([
        ("name", "=like", MO_NAME + "-%"),
    ])
    if backorders:
        failures.append(
            f"Unexpected backorder MO(s) created: {backorders.mapped('name')}"
        )

    return failures
