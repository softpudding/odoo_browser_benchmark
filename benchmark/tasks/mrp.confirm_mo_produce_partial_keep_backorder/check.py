"""Postcondition checks for mrp.confirm_mo_produce_partial_keep_backorder.

After the task, Odoo's `_split_productions` renames the original MO
from 'MO-BENCH-PARTIAL' to 'MO-BENCH-PARTIAL-001' (backorder_sequence=1)
and creates a sibling 'MO-BENCH-PARTIAL-002' (backorder_sequence=2) for
the remaining qty.

Validates:
  * The original MO (now named MO-BENCH-PARTIAL-001) is state='done'
    with product_qty=4 and qty_produced=4.
  * The backorder MO (MO-BENCH-PARTIAL-002) is state in
    ('confirmed','to_close','progress') with product_qty=6.
  * Both share the same production_group_id / procurement_group_id
    (via the auto-created `production_group_id` linkage).
  * No stray MOs for Bench Widget.
"""

MO_NAME = "MO-BENCH-PARTIAL"
ORIG_RENAMED = "MO-BENCH-PARTIAL-001"
BACKORDER_NAME = "MO-BENCH-PARTIAL-002"
FINISHED = "Bench Widget"
COMPONENT = "Bench Mat"


def check(env):
    failures = []

    # The original MO may survive under its original name if the agent
    # did NOT trigger the backorder split (a regression); in that case
    # report it clearly.
    still_original = env["mrp.production"].search(
        [("name", "=", MO_NAME)], limit=1
    )
    if still_original:
        # It never got renamed — the split didn't happen, or the user
        # cancelled / discarded the backorder wizard.
        return [
            f"Manufacturing order {MO_NAME!r} still exists under its "
            f"original name (state={still_original.state!r}). Expected it "
            f"to have been renamed to {ORIG_RENAMED!r} by Odoo's backorder "
            f"split after clicking the primary 'Create backorder' button."
        ]

    orig = env["mrp.production"].search(
        [("name", "=", ORIG_RENAMED)], limit=1
    )
    if not orig:
        return [
            f"Original (renamed) manufacturing order {ORIG_RENAMED!r} not "
            f"found — the 'Create backorder' flow never ran."
        ]

    # --- Original MO state + qty after split ---
    if orig.state == "cancel":
        failures.append(
            f"Original MO {ORIG_RENAMED!r} is cancelled — the task must "
            f"finish it, not cancel it"
        )
    elif orig.state != "done":
        failures.append(
            f"Original MO {ORIG_RENAMED!r} state is {orig.state!r}, "
            f"expected 'done'"
        )
    if abs((orig.qty_produced or 0.0) - 4.0) > 1e-6:
        failures.append(
            f"Original MO qty_produced is {orig.qty_produced}, expected 4.0"
        )
    if abs((orig.product_qty or 0.0) - 4.0) > 1e-6:
        failures.append(
            f"Original MO product_qty is {orig.product_qty}, expected 4.0 "
            f"(Odoo rewrites product_qty to the actually-produced qty when "
            f"a backorder is created)"
        )
    if orig.product_id.name != FINISHED:
        failures.append(
            f"Original MO product is {orig.product_id.name!r}, expected "
            f"{FINISHED!r}"
        )
    if (orig.backorder_sequence or 0) != 1:
        failures.append(
            f"Original MO backorder_sequence is {orig.backorder_sequence}, "
            f"expected 1"
        )

    # --- Backorder sibling ---
    bo = env["mrp.production"].search(
        [("name", "=", BACKORDER_NAME)], limit=1
    )
    if not bo:
        # Maybe the sequence got higher than 002 (unlikely), grep by prefix.
        bo_candidates = env["mrp.production"].search([
            ("name", "=like", MO_NAME + "-%"),
            ("id", "!=", orig.id),
        ])
        if not bo_candidates:
            return failures + [
                f"No backorder MO was created (expected {BACKORDER_NAME!r}). "
                f"The task requires clicking the primary 'Create backorder' "
                f"button on the production-backorder wizard."
            ]
        if len(bo_candidates) > 1:
            failures.append(
                f"Expected exactly 1 backorder, found {len(bo_candidates)}: "
                f"{bo_candidates.mapped('name')}"
            )
        bo = bo_candidates[0]

    if bo.state not in ("confirmed", "to_close", "progress"):
        failures.append(
            f"Backorder MO {bo.name!r} state is {bo.state!r}, expected "
            f"one of ('confirmed', 'to_close', 'progress') — it must "
            f"remain open, not be cancelled or marked done."
        )
    if abs((bo.product_qty or 0.0) - 6.0) > 1e-6:
        failures.append(
            f"Backorder MO {bo.name!r} product_qty is {bo.product_qty}, "
            f"expected 6.0"
        )
    if bo.product_id.name != FINISHED:
        failures.append(
            f"Backorder MO product is {bo.product_id.name!r}, expected "
            f"{FINISHED!r}"
        )
    if (bo.backorder_sequence or 0) < 2:
        failures.append(
            f"Backorder MO {bo.name!r} backorder_sequence is "
            f"{bo.backorder_sequence}, expected >= 2"
        )

    # --- Original + backorder share the production group ---
    if orig.production_group_id and bo.production_group_id:
        if orig.production_group_id.id != bo.production_group_id.id:
            failures.append(
                f"production_group_id differs: original="
                f"{orig.production_group_id.id}, backorder="
                f"{bo.production_group_id.id}. Expected shared group."
            )

    # --- No stray MOs for Bench Widget ---
    all_widget_mos = env["mrp.production"].search([
        ("product_id", "=", orig.product_id.id),
    ])
    expected_ids = set(orig.ids) | set(bo.ids)
    extra = all_widget_mos.filtered(lambda m: m.id not in expected_ids)
    if extra:
        failures.append(
            f"Unexpected extra MOs for {FINISHED!r}: {extra.mapped('name')}"
        )

    return failures
