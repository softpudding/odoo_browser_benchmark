"""Postcondition checks for mrp.create_mo_consume_produce_done."""


def check(env):
    mos = env["mrp.production"].search([("product_id.display_name", "=", "Bench Power Pack")], order="id desc")
    if len(mos) != 1:
        return [f"Expected exactly one MO for Bench Power Pack, found {len(mos)}"]

    mo = mos[0]
    failures = []
    if mo.bom_id.code != "BOM-BPP-01":
        failures.append(f"MO uses BoM {mo.bom_id.code!r}, expected 'BOM-BPP-01'")
    if abs(mo.product_qty - 4.0) > 0.01:
        failures.append(f"MO quantity is {mo.product_qty}, expected 4.0")
    if mo.state != "done":
        failures.append(f"MO state is {mo.state!r}, expected 'done'")
    if abs(mo.qty_produced - 4.0) > 0.01:
        failures.append(f"Produced quantity is {mo.qty_produced}, expected 4.0")
    return failures
