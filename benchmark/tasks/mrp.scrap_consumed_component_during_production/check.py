"""Postcondition checks for mrp.scrap_consumed_component_during_production.

Validates:
  * MO MO-BENCH-SCRAP ends in state='done' with 1 unit produced.
  * Exactly one stock.scrap linked to that MO, state='done', product=Bench
    Screw, scrap_qty=1.
  * MO product and planned qty unchanged.
  * No extra MOs were created.
"""

MO_NAME = "MO-BENCH-SCRAP"
FINISHED = "Bench Assembly Kit"
COMPONENT = "Bench Screw"


def check(env):
    failures = []

    mo = env["mrp.production"].search([("name", "=", MO_NAME)], limit=1)
    if not mo:
        return [f"Manufacturing order {MO_NAME!r} not found"]

    if mo.state == "cancel":
        failures.append(
            f"MO {MO_NAME} is cancelled — the task must finish it, not cancel it"
        )
    elif mo.state != "done":
        failures.append(
            f"MO state is {mo.state!r}, expected 'done'"
        )

    if abs((mo.qty_produced or 0.0) - 1.0) > 1e-6:
        failures.append(
            f"MO qty_produced is {mo.qty_produced}, expected 1.0"
        )
    if abs((mo.product_qty or 0.0) - 1.0) > 1e-6:
        failures.append(
            f"MO product_qty is {mo.product_qty}, expected 1.0"
        )
    if mo.product_id.name != FINISHED:
        failures.append(
            f"MO product_id is {mo.product_id.name!r}, expected {FINISHED!r}"
        )

    # Scrap records linked to this MO.
    scraps = env["stock.scrap"].search([("production_id", "=", mo.id)])
    if not scraps:
        return failures + [
            f"No stock.scrap linked to MO {MO_NAME} — the task requires "
            f"scrapping 1 {COMPONENT} before marking the MO done"
        ]
    if len(scraps) > 1:
        failures.append(
            f"Expected exactly 1 scrap for MO {MO_NAME}, found "
            f"{len(scraps)}: {scraps.mapped('name')}"
        )

    s = scraps[0]
    if s.state != "done":
        failures.append(
            f"Scrap {s.name} state is {s.state!r}, expected 'done' "
            f"(the scrap wizard must be validated)"
        )
    if s.product_id.name != COMPONENT:
        failures.append(
            f"Scrap product is {s.product_id.name!r}, expected {COMPONENT!r}"
        )
    if abs((s.scrap_qty or 0.0) - 1.0) > 1e-6:
        failures.append(
            f"Scrap quantity is {s.scrap_qty}, expected 1.0"
        )

    # Source location must be an 'internal' stock location (WH/Stock),
    # NOT the scrap/virtual location.
    if s.location_id and s.location_id.usage != "internal":
        failures.append(
            f"Scrap source location is {s.location_id.display_name!r} "
            f"(usage={s.location_id.usage}); expected an internal stock "
            f"location like WH/Stock"
        )

    # No stray MOs for this finished product.
    other_mos = env["mrp.production"].search([
        ("product_id", "=", mo.product_id.id),
        ("id", "!=", mo.id),
    ])
    if other_mos:
        failures.append(
            f"Unexpected extra MOs for {FINISHED!r}: "
            f"{other_mos.mapped('name')}"
        )

    return failures
