"""Postcondition checks for mrp.scrap_component_during_production.

Validates:
  * Exactly one stock.scrap exists for MO M-BENCH-PROD-001.
  * That scrap is in 'done' state, product Bench Component A, qty=2.
  * The MO is 'done' with qty_produced == 5 and product_qty unchanged.
  * No stray scraps target Bench Component B (distractor).
  * No extra MOs for Bench Final Product were created.
"""

MO_NAME = "M-BENCH-PROD-001"
FINISHED = "Bench Final Product"
COMP_A = "Bench Component A"
COMP_B = "Bench Component B"


def check(env):
    failures = []

    mo = env["mrp.production"].search([("name", "=", MO_NAME)], limit=1)
    if not mo:
        return [f"Manufacturing order '{MO_NAME}' not found"]

    # MO state + produced quantity.
    if mo.state == "cancel":
        failures.append(
            f"MO {MO_NAME} is cancelled — the task must finish it, not cancel it"
        )
    elif mo.state != "done":
        failures.append(f"MO state is '{mo.state}', expected 'done'")

    if abs((mo.qty_produced or 0.0) - 5.0) > 1e-6:
        failures.append(
            f"MO qty_produced is {mo.qty_produced}, expected 5.0"
        )
    if abs((mo.product_qty or 0.0) - 5.0) > 1e-6:
        failures.append(
            f"MO product_qty changed to {mo.product_qty}, expected 5.0"
        )
    if mo.product_id.name != FINISHED:
        failures.append(
            f"MO product_id is '{mo.product_id.name}', expected '{FINISHED}'"
        )

    # Scrap records for this MO.
    scraps = env["stock.scrap"].search([("production_id", "=", mo.id)])
    if not scraps:
        return failures + [
            f"No stock.scrap linked to MO {MO_NAME} — the task requires "
            f"scrapping 2 {COMP_A} before production"
        ]
    if len(scraps) > 1:
        failures.append(
            f"Expected exactly 1 scrap for MO {MO_NAME}, found "
            f"{len(scraps)}: {scraps.mapped('name')}"
        )
    s = scraps[0]

    if s.state != "done":
        failures.append(
            f"Scrap {s.name} state is '{s.state}', expected 'done' "
            f"(the scrap wizard must be validated)"
        )
    if s.product_id.name != COMP_A:
        failures.append(
            f"Scrap product is '{s.product_id.name}', expected '{COMP_A}' "
            f"— the agent scrapped the wrong component"
        )
    if abs((s.scrap_qty or 0.0) - 2.0) > 1e-6:
        failures.append(
            f"Scrap quantity is {s.scrap_qty}, expected 2.0"
        )

    # Make sure no stray MOs for this product were created.
    other_mos = env["mrp.production"].search([
        ("product_id", "=", mo.product_id.id),
        ("id", "!=", mo.id),
    ])
    if other_mos:
        failures.append(
            f"Unexpected extra MOs for '{FINISHED}': "
            f"{other_mos.mapped('name')}"
        )

    # Make sure nobody scrapped the distractor component.
    comp_b_prod = env["product.product"].search([("name", "=", COMP_B)], limit=1)
    if comp_b_prod:
        b_scraps = env["stock.scrap"].search([
            ("product_id", "=", comp_b_prod.id),
            ("production_id", "=", mo.id),
        ])
        if b_scraps:
            failures.append(
                f"Unexpected scrap(s) for distractor '{COMP_B}': "
                f"{b_scraps.mapped('name')}"
            )

    return failures
