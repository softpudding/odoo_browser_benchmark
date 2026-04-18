"""Postcondition checks for mrp.scrap_component_during_partial_production.

Validates:
  * Exactly one stock.scrap exists for MO M-BENCH-SCRAP-001.
  * The scrap is in 'done' state with product ScrewA, qty=2.
  * The scrap carries the 'Defective batch' reason tag.
  * The MO is in 'done' state with qty_produced == 5.
  * No extra MOs / scraps were created, the original MO wasn't cancelled.
"""

MO_NAME = "M-BENCH-SCRAP-001"
FINISHED = "Bench Widget"
COMP_A = "ScrewA"
REASON_TAG = "Defective batch"


def check(env):
    failures = []

    mo = env["mrp.production"].search([("name", "=", MO_NAME)], limit=1)
    if not mo:
        return [f"Manufacturing order '{MO_NAME}' not found"]

    # MO state + produced quantity.
    if mo.state == "cancel":
        failures.append(f"MO {MO_NAME} is cancelled — the task must finish it, not cancel it")
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
            f"scrapping 2 ScrewA before production"
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
    tag_names = s.scrap_reason_tag_ids.mapped("name")
    if REASON_TAG not in tag_names:
        failures.append(
            f"Scrap reason tags {tag_names!r} do not include "
            f"'{REASON_TAG}'"
        )

    # Source location must be an 'internal' stock location (WH/Stock),
    # NOT the scrap/virtual location.
    if s.location_id and s.location_id.usage != "internal":
        failures.append(
            f"Scrap source location is '{s.location_id.display_name}' "
            f"(usage={s.location_id.usage}); expected an internal stock "
            f"location like WH/Stock"
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

    return failures
