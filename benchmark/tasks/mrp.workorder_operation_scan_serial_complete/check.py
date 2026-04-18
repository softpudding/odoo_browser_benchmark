"""Postcondition check for mrp.workorder_operation_scan_serial_complete.

Validates that:
  - MO 'MO-BENCH-WO' exists and is in state 'done'.
  - The MO's single work order 'Final Assembly' (on WC-01) is in state 'done'.
  - The produced qty on the MO is 1.0.
  - Exactly ONE stock.move.line with lot_id = SN-B on the Bench Serial Part
    raw move, with quantity == 1 and picked == True.
  - SN-A, SN-C, SN-D are still available (qty_available == 1 at WH/Stock).
  - No backorder MO with the same prefix was created.
"""


MO_NAME = "MO-BENCH-WO"
FINISHED_NAME = "Bench Assembly Kit"
COMPONENT_NAME = "Bench Serial Part"
WORKCENTER_NAME = "WC-01"
OPERATION_NAME = "Final Assembly"
REQUIRED_SERIAL = "SN-B"
OTHER_SERIALS = ["SN-A", "SN-C", "SN-D"]


def check(env):
    failures = []

    mos = env["mrp.production"].search([("name", "=", MO_NAME)])
    if not mos:
        return [f"Manufacturing order {MO_NAME!r} not found"]
    if len(mos) > 1:
        failures.append(f"Expected exactly 1 MO named {MO_NAME!r}, got {len(mos)}")
    mo = mos[0]

    if mo.state != "done":
        failures.append(
            f"MO state is {mo.state!r}, expected 'done'"
        )

    if abs(mo.qty_produced - 1.0) > 1e-6:
        failures.append(
            f"MO qty_produced is {mo.qty_produced}, expected 1.0"
        )

    # --- Work order lifecycle ---
    if len(mo.workorder_ids) != 1:
        failures.append(
            f"Expected exactly 1 work order, got {len(mo.workorder_ids)}"
        )
    else:
        wo = mo.workorder_ids[0]
        if wo.state != "done":
            failures.append(
                f"Work order state is {wo.state!r}, expected 'done'"
            )
        if wo.workcenter_id.name != WORKCENTER_NAME:
            failures.append(
                f"Work order workcenter is {wo.workcenter_id.name!r}, "
                f"expected {WORKCENTER_NAME!r}"
            )
        if wo.operation_id and wo.operation_id.name != OPERATION_NAME:
            failures.append(
                f"Work order operation is {wo.operation_id.name!r}, "
                f"expected {OPERATION_NAME!r}"
            )

    # --- Serial consumption: SN-B only ---
    comp_moves = mo.move_raw_ids.filtered(
        lambda m: m.product_id.name == COMPONENT_NAME
    )
    if not comp_moves:
        failures.append(
            f"No raw move for component {COMPONENT_NAME!r} on the MO"
        )
    else:
        # move_line_ids for the component raw move(s)
        all_mls = comp_moves.mapped("move_line_ids")
        consumed_mls = all_mls.filtered(
            lambda ml: ml.quantity > 0 and ml.picked
        )
        consumed_lots = consumed_mls.mapped("lot_id")
        consumed_lot_names = sorted(consumed_lots.mapped("name"))

        if consumed_lot_names != [REQUIRED_SERIAL]:
            failures.append(
                f"Expected exactly [{REQUIRED_SERIAL!r}] consumed, got "
                f"{consumed_lot_names} (all move lines: "
                f"{[(ml.lot_id.name, ml.quantity, ml.picked) for ml in all_mls]})"
            )

        total_qty = sum(consumed_mls.mapped("quantity"))
        if abs(total_qty - 1.0) > 1e-6:
            failures.append(
                f"Total consumed quantity for {COMPONENT_NAME!r} is "
                f"{total_qty}, expected 1.0"
            )

    # --- Other serials still present at WH/Stock (quantity on-hand == 1) ---
    # After the MO is Done, only SN-B should have been consumed. The
    # other three serials must still have 1.0 on-hand at WH/Stock.
    component = env["product.product"].search(
        [("name", "=", COMPONENT_NAME)], limit=1,
    )
    warehouse = env["stock.warehouse"].search(
        [("company_id", "=", env.company.id)], limit=1,
    )
    stock_loc = warehouse.lot_stock_id
    if component and stock_loc:
        for sn in OTHER_SERIALS:
            lot = env["stock.lot"].search([
                ("name", "=", sn),
                ("product_id", "=", component.id),
            ], limit=1)
            if not lot:
                failures.append(f"Serial {sn!r} missing from stock.lot")
                continue
            quants = env["stock.quant"].search([
                ("product_id", "=", component.id),
                ("lot_id", "=", lot.id),
                ("location_id", "=", stock_loc.id),
            ])
            on_hand = sum(quants.mapped("quantity"))
            if abs(on_hand - 1.0) > 1e-6:
                failures.append(
                    f"Serial {sn!r} has quantity={on_hand} at WH/Stock, "
                    f"expected 1.0 (must not have been consumed)"
                )

    # --- No backorder MOs ---
    backorders = env["mrp.production"].search([
        ("name", "=like", MO_NAME + "-%"),
    ])
    if backorders:
        failures.append(
            f"Unexpected backorder MO(s): {backorders.mapped('name')}"
        )

    return failures
