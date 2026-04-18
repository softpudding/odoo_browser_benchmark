"""Postcondition checks for mrp.create_mo_consume_produce_done.

Validates:
  * Exactly one MO exists for Bench Assembly.
  * MO state='done', product_qty=3.0, qty_produced=3.0.
  * The raw-material moves consumed 3 Bench Part A and 6 Bench Part B.
  * A finished stock.move produced 3 Bench Assembly.
  * No unbuild / scrap records were created.
"""

FINISHED = "Bench Assembly"
PART_A = "Bench Part A"
PART_B = "Bench Part B"


def check(env):
    failures = []

    finished = env["product.product"].search(
        [("name", "=", FINISHED)], limit=1
    )
    if not finished:
        return [f"Finished product '{FINISHED}' missing after run"]
    part_a = env["product.product"].search([("name", "=", PART_A)], limit=1)
    part_b = env["product.product"].search([("name", "=", PART_B)], limit=1)
    if not part_a or not part_b:
        failures.append("Component product(s) missing after run")

    mos = env["mrp.production"].search([("product_id", "=", finished.id)])
    if not mos:
        return failures + [
            f"No manufacturing order for '{FINISHED}' found — the task "
            f"requires creating and closing one MO from scratch"
        ]
    if len(mos) > 1:
        failures.append(
            f"Expected exactly 1 MO for '{FINISHED}', found "
            f"{len(mos)}: {mos.mapped('name')}"
        )
    mo = mos[0]

    if mo.state == "cancel":
        failures.append(
            f"MO '{mo.name}' is cancelled — the task must finish it, "
            f"not cancel it"
        )
    elif mo.state != "done":
        failures.append(
            f"MO '{mo.name}' state is '{mo.state}', expected 'done'"
        )

    if abs((mo.product_qty or 0.0) - 3.0) > 1e-6:
        failures.append(
            f"MO product_qty is {mo.product_qty}, expected 3.0"
        )
    if abs((mo.qty_produced or 0.0) - 3.0) > 1e-6:
        failures.append(
            f"MO qty_produced is {mo.qty_produced}, expected 3.0"
        )

    # Raw material moves.
    if part_a:
        raw_a = mo.move_raw_ids.filtered(
            lambda m: m.product_id.id == part_a.id
        )
        if not raw_a:
            failures.append(
                f"No raw-material move for '{PART_A}' on MO '{mo.name}'"
            )
        else:
            qty_a = sum(raw_a.mapped("quantity"))
            if abs(qty_a - 3.0) > 1e-6:
                failures.append(
                    f"Consumed quantity for '{PART_A}' is {qty_a}, expected 3.0"
                )

    if part_b:
        raw_b = mo.move_raw_ids.filtered(
            lambda m: m.product_id.id == part_b.id
        )
        if not raw_b:
            failures.append(
                f"No raw-material move for '{PART_B}' on MO '{mo.name}'"
            )
        else:
            qty_b = sum(raw_b.mapped("quantity"))
            if abs(qty_b - 6.0) > 1e-6:
                failures.append(
                    f"Consumed quantity for '{PART_B}' is {qty_b}, expected 6.0"
                )

    # Finished-goods move.
    finished_moves = mo.move_finished_ids.filtered(
        lambda m: m.product_id.id == finished.id
    )
    if not finished_moves:
        failures.append(
            f"No finished-goods move for '{FINISHED}' on MO '{mo.name}'"
        )
    else:
        qty_f = sum(finished_moves.mapped("quantity"))
        if abs(qty_f - 3.0) > 1e-6:
            failures.append(
                f"Produced quantity for '{FINISHED}' is {qty_f}, expected 3.0"
            )

    # No unbuild / scrap records.
    unbuilds = env["mrp.unbuild"].search([("mo_id", "=", mo.id)])
    if unbuilds:
        failures.append(
            f"Unexpected unbuild order(s) for MO '{mo.name}': "
            f"{unbuilds.mapped('name')}"
        )
    scraps = env["stock.scrap"].search([("production_id", "=", mo.id)])
    if scraps:
        failures.append(
            f"Unexpected scrap(s) for MO '{mo.name}': "
            f"{scraps.mapped('name')}"
        )

    return failures
