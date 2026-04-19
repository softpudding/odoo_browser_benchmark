"""Postcondition checks for stock.cancel_picking_abandoned.

Validates:
1. The seeded picking WH/OUT/BENCH-CANCEL still exists (not deleted).
2. Its state is 'cancel'.
3. Partner is still Bench Cancel Ship Co and the single move line for
   Bench Cancel Prod with demand=3 is unchanged.
4. Exactly ONE outgoing picking exists for Bench Cancel Ship Co (no new
   replacement / return / backorder created).
"""

PICKING_NAME = "WH/OUT/BENCH-CANCEL"
CUSTOMER_NAME = "Bench Cancel Ship Co"
PRODUCT_NAME = "Bench Cancel Prod"
EXPECTED_DEMAND = 3.0


def check(env):
    failures = []

    customer = env["res.partner"].search(
        [("name", "=", CUSTOMER_NAME)], limit=1
    )
    if not customer:
        return [f"Customer '{CUSTOMER_NAME}' missing (seed artefact deleted)"]

    product = env["product.product"].search(
        [("name", "=", PRODUCT_NAME)], limit=1
    )
    if not product:
        return [f"Product '{PRODUCT_NAME}' missing (seed artefact deleted)"]

    picking = env["stock.picking"].with_context(active_test=False).search(
        [("name", "=", PICKING_NAME)], limit=1
    )
    if not picking:
        return [
            f"Picking '{PICKING_NAME}' not found (must exist in state='cancel', "
            f"NOT deleted)"
        ]

    if picking.state != "cancel":
        failures.append(
            f"Picking '{PICKING_NAME}' state is '{picking.state}', expected 'cancel'"
        )

    if picking.partner_id.id != customer.id:
        failures.append(
            f"Picking partner is '{picking.partner_id.display_name}', "
            f"expected '{CUSTOMER_NAME}' (do not modify partner)"
        )

    if picking.picking_type_id.code != "outgoing":
        failures.append(
            f"Picking type code is '{picking.picking_type_id.code}', expected 'outgoing'"
        )

    # Move(s) on the picking: exactly one for Bench Cancel Prod, demand=3.
    moves = picking.move_ids
    if len(moves) != 1:
        failures.append(
            f"Picking has {len(moves)} moves, expected 1 (do not modify lines)"
        )
    else:
        mv = moves[0]
        if mv.product_id.id != product.id:
            failures.append(
                f"Move product is '{mv.product_id.display_name}', "
                f"expected '{PRODUCT_NAME}'"
            )
        if abs(mv.product_uom_qty - EXPECTED_DEMAND) > 0.001:
            failures.append(
                f"Move demand is {mv.product_uom_qty}, expected {EXPECTED_DEMAND}"
            )

    # No extra outgoing pickings for this customer (no replacement / return).
    all_out = env["stock.picking"].with_context(active_test=False).search([
        ("partner_id", "=", customer.id),
        ("picking_type_id.code", "=", "outgoing"),
    ])
    if len(all_out) != 1:
        failures.append(
            f"Expected exactly 1 outgoing picking for '{CUSTOMER_NAME}', "
            f"found {len(all_out)} (names: {all_out.mapped('name')}). "
            f"Do not create a replacement, return, or backorder."
        )

    return failures
