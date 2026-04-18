"""Postcondition checks for purchase_stock.return_partial_with_distractor_lines."""


TARGET_ORIGIN = "P-BENCH-RET-001"


def check(env):
    failures = []

    target = env["purchase.order"].search([("origin", "=", TARGET_ORIGIN)], limit=1)
    if not target:
        return [f"Target purchase order {TARGET_ORIGIN!r} not found"]

    # Original receipt should still be done
    original_receipts = target.picking_ids.filtered(lambda p: not p.return_id)
    if len(original_receipts) != 1:
        failures.append(
            f"Expected exactly 1 original receipt, found {len(original_receipts)}"
        )
    else:
        orig = original_receipts[0]
        if orig.state != "done":
            failures.append(
                f"Original receipt state is {orig.state!r}, expected 'done'"
            )

    # PO line received quantities: WidgetB went from 5 to 3 after the return,
    # WidgetA stays at 10, WidgetC stays at 8.
    expected_qty = {
        "Bayside WidgetA": 10.0,
        "Bayside WidgetB": 3.0,
        "Bayside WidgetC": 8.0,
    }
    for line in target.order_line:
        exp = expected_qty.get(line.product_id.name)
        if exp is None:
            failures.append(f"Unexpected target PO line {line.product_id.name!r}")
            continue
        if abs(float(line.qty_received or 0.0) - exp) > 0.001:
            failures.append(
                f"{line.product_id.name} received qty is {line.qty_received}, expected {exp}"
            )

    # Exactly one return picking, validated, with WidgetB=2 only
    return_pickings = target.picking_ids.filtered(lambda p: p.return_id)
    if len(return_pickings) != 1:
        failures.append(
            f"Expected exactly 1 return picking, found {len(return_pickings)}"
        )
    else:
        picking = return_pickings[0]
        if picking.state != "done":
            failures.append(
                f"Return picking state is {picking.state!r}, expected 'done'"
            )

        active_moves = picking.move_ids.filtered(lambda m: m.state != "cancel")
        actual_names = {m.product_id.name for m in active_moves}

        # WidgetB must be present with quantity 2
        widget_b_moves = active_moves.filtered(
            lambda m: m.product_id.name == "Bayside WidgetB"
        )
        if not widget_b_moves:
            failures.append("Bayside WidgetB is missing from the return picking")
        else:
            total_b = sum(float(m.quantity or 0.0) for m in widget_b_moves)
            if abs(total_b - 2.0) > 0.001:
                failures.append(
                    f"Bayside WidgetB return quantity is {total_b}, expected 2.0"
                )

        # WidgetA and WidgetC must NOT be on the return (or must have quantity 0)
        for forbidden in ("Bayside WidgetA", "Bayside WidgetC"):
            if forbidden in actual_names:
                forbidden_moves = active_moves.filtered(
                    lambda m, fn=forbidden: m.product_id.name == fn
                )
                total_qty = sum(float(m.quantity or 0.0) for m in forbidden_moves)
                if total_qty > 0.001:
                    failures.append(
                        f"{forbidden} appears on return with quantity {total_qty}, expected 0 or absent"
                    )

    return failures
