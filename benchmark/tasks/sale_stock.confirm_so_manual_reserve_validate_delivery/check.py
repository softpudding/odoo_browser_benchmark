"""Postcondition checks for sale_stock.confirm_so_manual_reserve_validate_delivery.

Validates:
1. SO for "Bench SO Customer" is confirmed (state='sale') with 5 units of
   Bench Stockable Product at $20.00 each.
2. Linked outgoing delivery (stock.picking, picking_type_code='outgoing')
   is validated (state='done') with 5 units delivered.
3. No backorder was created (only one picking on the SO).
"""


def check(env):
    failures = []

    partner = env["res.partner"].search(
        [("name", "=", "Bench SO Customer")], limit=1
    )
    if not partner:
        return ["Partner 'Bench SO Customer' not found"]

    so = env["sale.order"].search(
        [("partner_id", "=", partner.id)], limit=1
    )
    if not so:
        return ["Target SO for 'Bench SO Customer' not found"]

    # --- 1. SO confirmed ---
    if so.state != "sale":
        failures.append(f"SO state is '{so.state}', expected 'sale'")

    # Verify order content hasn't been altered
    if len(so.order_line) != 1:
        failures.append(
            f"SO has {len(so.order_line)} lines, expected 1"
        )
    else:
        line = so.order_line[0]
        if line.product_id.name != "Bench Stockable Product":
            failures.append(
                f"SO line product is '{line.product_id.name}', "
                "expected 'Bench Stockable Product'"
            )
        if abs(line.product_uom_qty - 5.0) > 0.001:
            failures.append(
                f"SO line quantity is {line.product_uom_qty}, expected 5"
            )
        if abs(line.price_unit - 20.00) > 0.001:
            failures.append(
                f"SO line price is {line.price_unit}, expected 20.00"
            )

    # --- 2. Delivery picking done ---
    pickings = so.picking_ids
    if not pickings:
        return failures + ["No delivery picking found for the SO"]

    outgoing = pickings.filtered(lambda p: p.picking_type_code == "outgoing")
    if not outgoing:
        return failures + ["No outgoing delivery picking found"]

    done_pickings = outgoing.filtered(lambda p: p.state == "done")
    if not done_pickings:
        states = ", ".join(sorted({p.state for p in outgoing}))
        failures.append(
            f"No validated (done) delivery — picking states: {states}"
        )
    else:
        picking = done_pickings[0]
        moves = picking.move_ids
        bench_moves = moves.filtered(
            lambda m: m.product_id.name == "Bench Stockable Product"
        )
        if not bench_moves:
            failures.append(
                "Bench Stockable Product move missing from the done delivery"
            )
        else:
            move = bench_moves[0]
            qty = getattr(move, "quantity", None)
            if qty is None:
                qty = getattr(move, "quantity_done", 0.0)
            if abs(qty - 5.0) > 0.001:
                failures.append(
                    f"Delivered quantity is {qty}, expected 5.0"
                )

    # --- 3. No backorder ---
    non_done = outgoing.filtered(lambda p: p.state != "done")
    if non_done:
        failures.append(
            "Unexpected additional outgoing picking(s) exist "
            f"(states: {[p.state for p in non_done]}) — no backorder "
            "should have been created"
        )

    return failures
