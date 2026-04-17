"""Postcondition checks for sale_stock.confirm_order_deliver_partial_backorder.

Validates:
1. SO with client_order_ref "BENCH-SO-BACK" is confirmed (state='sale').
2. Original delivery is validated (state='done') with correct partial qtys.
3. A backorder exists (state='assigned' or 'waiting') with remaining qtys:
   - Precision Bearing Kit: 10 remaining (25 - 15)
   - Titanium Bolt Set M12: 14 remaining (20 - 6)
   - Stainless Steel Rod 2m NOT in backorder (fully shipped: 40/40)
4. Distractor SO "BENCH-SO-BACK-DIST" is still draft.
"""


def check(env):
    failures = []

    # --- 1. SO confirmed ---
    so = env["sale.order"].search(
        [("client_order_ref", "=", "BENCH-SO-BACK")], limit=1
    )
    if not so:
        return ["Target SO 'BENCH-SO-BACK' not found"]

    if so.state != "sale":
        failures.append(
            f"SO state is '{so.state}', expected 'sale'"
        )

    # --- 2. Find pickings linked to this SO ---
    pickings = so.picking_ids
    if not pickings:
        return failures + ["No delivery orders found for the SO"]

    done_pickings = pickings.filtered(lambda p: p.state == "done")
    backorder_pickings = pickings.filtered(
        lambda p: p.state in ("assigned", "waiting", "confirmed")
    )

    if not done_pickings:
        failures.append(
            "No validated (done) delivery found — expected the partial "
            "delivery to be validated"
        )

    if not backorder_pickings:
        failures.append(
            "No backorder delivery found — expected a backorder with "
            "remaining quantities"
        )

    # --- 3. Validate done delivery quantities ---
    if done_pickings:
        done_picking = done_pickings[0]
        moves = done_picking.move_ids

        bearing = moves.filtered(
            lambda m: "Bearing" in m.product_id.name
        )
        rod = moves.filtered(
            lambda m: "Steel Rod" in m.product_id.name
        )
        bolt = moves.filtered(
            lambda m: "Bolt" in m.product_id.name
        )

        if bearing:
            qty = getattr(bearing, "quantity", None)
            if qty is None:
                qty = bearing.quantity_done
            if abs(qty - 15) > 0.001:
                failures.append(
                    f"Precision Bearing Kit done qty is {qty}, expected 15"
                )
        else:
            failures.append(
                "Precision Bearing Kit move missing from done delivery"
            )

        if rod:
            qty = getattr(rod, "quantity", None)
            if qty is None:
                qty = rod.quantity_done
            if abs(qty - 40) > 0.001:
                failures.append(
                    f"Stainless Steel Rod 2m done qty is {qty}, expected 40"
                )
        else:
            failures.append(
                "Stainless Steel Rod 2m move missing from done delivery"
            )

        if bolt:
            qty = getattr(bolt, "quantity", None)
            if qty is None:
                qty = bolt.quantity_done
            if abs(qty - 6) > 0.001:
                failures.append(
                    f"Titanium Bolt Set M12 done qty is {qty}, expected 6"
                )
        else:
            failures.append(
                "Titanium Bolt Set M12 move missing from done delivery"
            )

    # --- 4. Validate backorder quantities ---
    if backorder_pickings:
        bo = backorder_pickings[0]
        bo_moves = bo.move_ids

        bo_bearing = bo_moves.filtered(
            lambda m: "Bearing" in m.product_id.name
        )
        bo_bolt = bo_moves.filtered(
            lambda m: "Bolt" in m.product_id.name
        )
        bo_rod = bo_moves.filtered(
            lambda m: "Steel Rod" in m.product_id.name
        )

        if bo_bearing:
            demand = bo_bearing.product_uom_qty
            if abs(demand - 10) > 0.001:
                failures.append(
                    f"Backorder Bearing Kit demand is {demand}, expected 10"
                )
        else:
            failures.append(
                "Precision Bearing Kit missing from backorder"
            )

        if bo_bolt:
            demand = bo_bolt.product_uom_qty
            if abs(demand - 14) > 0.001:
                failures.append(
                    f"Backorder Titanium Bolt demand is {demand}, expected 14"
                )
        else:
            failures.append(
                "Titanium Bolt Set M12 missing from backorder"
            )

        if bo_rod:
            # Rod was fully shipped (40/40), should NOT be in backorder
            failures.append(
                "Stainless Steel Rod 2m should NOT be in backorder "
                "(fully shipped 40/40)"
            )

    # --- 5. Distractor SO unchanged ---
    dist = env["sale.order"].search(
        [("client_order_ref", "=", "BENCH-SO-BACK-DIST")], limit=1
    )
    if not dist:
        failures.append("Distractor SO 'BENCH-SO-BACK-DIST' is missing")
    elif dist.state != "draft":
        failures.append(
            f"Distractor SO state is '{dist.state}', expected 'draft'"
        )

    return failures
