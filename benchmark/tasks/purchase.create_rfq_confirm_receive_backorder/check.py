"""Postcondition checks for purchase.create_rfq_confirm_receive_backorder.

Validates:
1. PO with vendor reference SRC-PO-2026-Q2 exists, is confirmed, has vendor
   Summit Ridge Components, and has exactly 3 lines with correct products,
   quantities, and prices.
2. Original receipt is validated (state = done) with correct partial quantities.
3. A backorder receipt exists (state = assigned or waiting) with remaining
   quantities for Hydraulic Cylinder 50mm (8) and Flow Control Valve (7).
4. Pressure Gauge PSI is NOT in the backorder (fully received).
"""


def check(env):
    failures = []

    # --- Verify PO ---
    po = env["purchase.order"].search(
        [("partner_ref", "=", "SRC-PO-2026-Q2")], limit=1
    )
    if not po:
        return ["PO with vendor reference 'SRC-PO-2026-Q2' not found"]

    vendor = env["res.partner"].search(
        [("name", "=", "Summit Ridge Components")], limit=1
    )
    if not vendor:
        return ["Vendor 'Summit Ridge Components' not found"]

    if po.partner_id.id != vendor.id:
        failures.append(
            f"PO vendor is '{po.partner_id.display_name}', "
            "expected 'Summit Ridge Components'"
        )

    if po.state != "purchase":
        failures.append(
            f"PO state is '{po.state}', expected 'purchase' (confirmed)"
        )

    # --- Verify PO lines ---
    lines = po.order_line
    if len(lines) != 3:
        failures.append(
            f"PO has {len(lines)} lines, expected exactly 3"
        )
        return failures

    expected_lines = {
        "Hydraulic Cylinder 50mm": {"qty": 20, "price": 85.00},
        "Pressure Gauge PSI": {"qty": 30, "price": 24.50},
        "Flow Control Valve": {"qty": 15, "price": 112.00},
    }

    for name, expected in expected_lines.items():
        line = lines.filtered(lambda l, n=name: l.product_id.name == n)
        if not line:
            failures.append(f"PO is missing product line '{name}'")
            continue
        if len(line) > 1:
            failures.append(f"PO has {len(line)} lines for '{name}', expected 1")
            continue
        if abs(line.product_qty - expected["qty"]) > 0.001:
            failures.append(
                f"'{name}' quantity is {line.product_qty}, "
                f"expected {expected['qty']}"
            )
        if abs(line.price_unit - expected["price"]) > 0.01:
            failures.append(
                f"'{name}' unit price is {line.price_unit}, "
                f"expected {expected['price']}"
            )

    # --- Verify pickings ---
    pickings = env["stock.picking"].search([
        ("origin", "=", po.name),
    ], order="id asc")

    if len(pickings) < 2:
        failures.append(
            f"Expected at least 2 receipts (original + backorder), "
            f"found {len(pickings)}"
        )
        if len(pickings) == 1:
            if pickings.state == "done":
                failures.append(
                    "Only one receipt found and it is done — backorder was "
                    "likely not created (agent may have chosen 'No Backorder')"
                )
            else:
                failures.append(
                    f"Single receipt state is '{pickings.state}', expected "
                    "it to be validated with a backorder"
                )
        return failures

    # Find the original (done) receipt and the backorder
    done_pickings = pickings.filtered(lambda p: p.state == "done")
    backorder_pickings = pickings.filtered(
        lambda p: p.state in ("assigned", "waiting")
    )

    if not done_pickings:
        failures.append("No validated (done) receipt found")
    else:
        original = done_pickings[0]
        # Check partial quantities on the original receipt
        moves = original.move_ids
        expected_done = {
            "Hydraulic Cylinder 50mm": 12,
            "Pressure Gauge PSI": 30,
            "Flow Control Valve": 8,
        }
        for name, expected_qty in expected_done.items():
            move = moves.filtered(
                lambda m, n=name: m.product_id.name == n
            )
            if not move:
                failures.append(
                    f"Original receipt missing move for '{name}'"
                )
                continue
            qty = getattr(move, "quantity", None)
            if qty is None:
                qty = move.quantity_done
            if abs(qty - expected_qty) > 0.001:
                failures.append(
                    f"Original receipt '{name}' done qty is {qty}, "
                    f"expected {expected_qty}"
                )

    if not backorder_pickings:
        failures.append(
            "No backorder receipt found (expected state 'assigned' or 'waiting')"
        )
    else:
        backorder = backorder_pickings[0]

        # Verify backorder has a backorder_id (links to original)
        if not backorder.backorder_id:
            failures.append(
                "Backorder receipt does not have backorder_id set "
                "(not properly linked as a backorder)"
            )

        bo_moves = backorder.move_ids
        # Expected remaining: Hydraulic Cylinder 50mm = 8, Flow Control Valve = 7
        expected_backorder = {
            "Hydraulic Cylinder 50mm": 8,
            "Flow Control Valve": 7,
        }
        for name, expected_qty in expected_backorder.items():
            move = bo_moves.filtered(
                lambda m, n=name: m.product_id.name == n
            )
            if not move:
                failures.append(
                    f"Backorder missing move for '{name}' "
                    f"(expected remaining qty {expected_qty})"
                )
                continue
            demand = move.product_uom_qty
            if abs(demand - expected_qty) > 0.001:
                failures.append(
                    f"Backorder '{name}' demand is {demand}, "
                    f"expected {expected_qty}"
                )

        # Pressure Gauge PSI should NOT be in backorder (fully received)
        gauge_move = bo_moves.filtered(
            lambda m: m.product_id.name == "Pressure Gauge PSI"
        )
        if gauge_move:
            failures.append(
                "Pressure Gauge PSI should NOT be in backorder "
                "(it was fully received)"
            )

    return failures
