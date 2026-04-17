"""Postcondition checks for stock.return_delivery_create_credit_note.

Validates:
1. Original delivery BENCH-DEL-RET is still in state 'done'.
2. A return picking exists with Industrial Fan Unit qty = 4, state = 'done'.
3. No Rubber Gasket Set in the return picking.
4. A credit note (out_refund) exists and is posted.
5. Credit note amount corresponds to 4 x $180 = $720.
6. Distractor delivery BENCH-DEL-RET-DIST is unchanged.
"""

from datetime import date


def check(env):
    failures = []

    # ------------------------------------------------------------------
    # 1. Original delivery still done
    # ------------------------------------------------------------------
    original = env["stock.picking"].search([
        ("origin", "=", "BENCH-DEL-RET"),
        ("return_id", "=", False),
    ], limit=1)
    if not original:
        # Fallback: search by origin alone
        candidates = env["stock.picking"].search([
            ("origin", "=", "BENCH-DEL-RET"),
        ])
        original = candidates.filtered(lambda p: not p.return_id)[:1]

    if not original:
        return ["Original delivery 'BENCH-DEL-RET' not found"]

    if original.state != "done":
        failures.append(
            f"Original delivery state is '{original.state}', expected 'done'"
        )

    # ------------------------------------------------------------------
    # 2. Return picking exists and is done
    # ------------------------------------------------------------------
    return_picking = env["stock.picking"].search([
        ("return_id", "=", original.id),
    ], limit=1)
    if not return_picking:
        # Fallback: look for return of our delivery via origin pattern
        return_picking = env["stock.picking"].search([
            ("origin", "like", "Return of%"),
            ("origin", "like", original.name),
        ], limit=1)

    if not return_picking:
        failures.append("Return picking not found for original delivery")
        return failures

    if return_picking.state != "done":
        failures.append(
            f"Return picking state is '{return_picking.state}', expected 'done'"
        )

    # ------------------------------------------------------------------
    # 3. Return has Industrial Fan Unit qty = 4, no Rubber Gasket Set
    # ------------------------------------------------------------------
    return_moves = return_picking.move_ids
    fan_moves = return_moves.filtered(
        lambda m: m.product_id.name == "Industrial Fan Unit"
    )
    gasket_moves = return_moves.filtered(
        lambda m: m.product_id.name == "Rubber Gasket Set"
    )

    if not fan_moves:
        failures.append("Return picking has no 'Industrial Fan Unit' move")
    else:
        fan_qty = fan_moves[0].quantity
        if abs(fan_qty - 4.0) > 0.001:
            failures.append(
                f"Industrial Fan Unit return qty is {fan_qty}, expected 4.0"
            )

    if gasket_moves:
        # Check if qty is > 0 (a zero-qty move line is acceptable)
        gasket_qty = sum(m.quantity for m in gasket_moves)
        if gasket_qty > 0.001:
            failures.append(
                f"Rubber Gasket Set should NOT be returned, but found qty {gasket_qty}"
            )

    # ------------------------------------------------------------------
    # 4. Credit note exists and is posted
    # ------------------------------------------------------------------
    # Find the original SO
    so = env["sale.order"].search([
        ("client_order_ref", "=", "BENCH-DEL-RET"),
    ], limit=1)
    if not so:
        failures.append("Sales order 'BENCH-DEL-RET' not found")
        return failures

    # Credit notes are out_refund type linked to the SO
    credit_notes = so.invoice_ids.filtered(
        lambda m: m.move_type == "out_refund"
    )
    if not credit_notes:
        # Fallback: look for credit notes that reverse our invoice
        original_invoices = so.invoice_ids.filtered(
            lambda m: m.move_type == "out_invoice"
        )
        for inv in original_invoices:
            reversals = env["account.move"].search([
                ("reversed_entry_id", "=", inv.id),
                ("move_type", "=", "out_refund"),
            ])
            credit_notes |= reversals

    if not credit_notes:
        failures.append("Credit note (out_refund) not found for the sales order")
        return failures

    posted_cn = credit_notes.filtered(lambda m: m.state == "posted")
    if not posted_cn:
        failures.append(
            f"Credit note exists but state is "
            f"'{credit_notes[0].state}', expected 'posted'"
        )
        return failures

    cn = posted_cn[0]

    # ------------------------------------------------------------------
    # 5. Credit note amount ~ $720 (4 x $180)
    # ------------------------------------------------------------------
    expected_amount = 720.0
    if abs(cn.amount_total - expected_amount) > 1.0:
        failures.append(
            f"Credit note amount_total is {cn.amount_total}, "
            f"expected ~{expected_amount} (4 x $180)"
        )

    # ------------------------------------------------------------------
    # 6. Credit note date
    # ------------------------------------------------------------------
    expected_date = date(2026, 6, 8)
    if cn.invoice_date and cn.invoice_date != expected_date:
        failures.append(
            f"Credit note date is {cn.invoice_date}, expected {expected_date}"
        )

    # ------------------------------------------------------------------
    # 7. Distractor delivery unchanged
    # ------------------------------------------------------------------
    distractor = env["stock.picking"].search([
        ("origin", "=", "BENCH-DEL-RET-DIST"),
        ("return_id", "=", False),
    ], limit=1)
    if not distractor:
        failures.append("Distractor delivery 'BENCH-DEL-RET-DIST' missing")
    elif distractor.state != "done":
        failures.append(
            f"Distractor delivery state is '{distractor.state}', expected 'done'"
        )
    else:
        # Ensure no return was created for distractor
        dist_returns = env["stock.picking"].search([
            ("return_id", "=", distractor.id),
        ])
        if dist_returns:
            failures.append(
                "Distractor delivery has a return picking — it should be untouched"
            )

    return failures
