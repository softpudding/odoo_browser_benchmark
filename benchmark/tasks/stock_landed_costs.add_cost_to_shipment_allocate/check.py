"""Postcondition checks for stock_landed_costs.add_cost_to_shipment_allocate.

Validates:
  1. Exactly one stock.landed.cost in state='done' whose picking_ids
     includes the seeded receipt 'R-BENCH-LC-001' AND whose cost_lines
     reference the Freight product.
  2. The record has exactly ONE cost line: product=Freight,
     price_unit=45.0, split_method='by_quantity'.
  3. The record has exactly ONE valuation_adjustment_line linked to
     the 'Bench Import Item' move with quantity=3.0 and
     additional_landed_cost=45.0.
  4. amount_total == 45.0.
  5. The seeded receipt is still state='done' and wasn't modified.
"""

RECEIPT_REF = "R-BENCH-LC-001"
VENDOR_NAME = "Bench Import Vendor"
PRODUCT_NAME = "Bench Import Item"
FREIGHT_NAME = "Freight"
DEMAND_QTY = 3.0
COST_AMOUNT = 45.0


def check(env):
    failures = []

    freight = env["product.product"].search(
        [("name", "=", FREIGHT_NAME)], limit=1
    )
    if not freight:
        return [f"Freight product '{FREIGHT_NAME}' not found"]

    item = env["product.product"].search(
        [("name", "=", PRODUCT_NAME)], limit=1
    )
    if not item:
        return [f"Bench item '{PRODUCT_NAME}' not found"]

    receipt = env["stock.picking"].search(
        [("name", "=", RECEIPT_REF)], limit=1
    )
    if not receipt:
        return [f"Receipt '{RECEIPT_REF}' not found"]
    if receipt.state != "done":
        failures.append(
            f"Seeded receipt state is '{receipt.state}', expected 'done' "
            "(agent must not revert the receipt)"
        )

    # Locate the landed cost — by cost_line product_id == Freight AND
    # picking_ids containing the seeded receipt.
    lcs = env["stock.landed.cost"].search([
        ("picking_ids", "in", [receipt.id]),
        ("cost_lines.product_id", "=", freight.id),
    ])

    if not lcs:
        return failures + [
            "No stock.landed.cost found linking the seeded receipt "
            f"'{RECEIPT_REF}' to Freight — agent likely did not create "
            "or save the landed cost record."
        ]
    if len(lcs) > 1:
        failures.append(
            f"Expected exactly 1 stock.landed.cost, found {len(lcs)}: "
            f"{lcs.mapped('name')}"
        )
    lc = lcs[:1]

    # State must be 'done' (Posted).
    if lc.state != "done":
        failures.append(
            f"Landed cost state is '{lc.state}', expected 'done' "
            "(agent must click Validate after Compute)"
        )

    # Cost line checks.
    cost_lines = lc.cost_lines
    if len(cost_lines) != 1:
        failures.append(
            f"Landed cost has {len(cost_lines)} cost lines, expected 1"
        )
    else:
        cl = cost_lines[0]
        if cl.product_id.id != freight.id:
            failures.append(
                f"Cost line product is '{cl.product_id.display_name}', "
                f"expected '{FREIGHT_NAME}'"
            )
        if abs((cl.price_unit or 0.0) - COST_AMOUNT) > 1e-6:
            failures.append(
                f"Cost line price_unit is {cl.price_unit}, "
                f"expected {COST_AMOUNT}"
            )
        if cl.split_method != "by_quantity":
            failures.append(
                f"Cost line split_method is '{cl.split_method}', "
                "expected 'by_quantity' (Freight's default)"
            )

    # Valuation-adjustment-line checks.
    vals = lc.valuation_adjustment_lines
    if len(vals) != 1:
        failures.append(
            f"Landed cost has {len(vals)} valuation adjustment lines, "
            "expected 1 (one per receipt move). Agent likely skipped "
            "the Compute button."
        )
    else:
        v = vals[0]
        if v.product_id.id != item.id:
            failures.append(
                f"Adjustment line product is '{v.product_id.display_name}', "
                f"expected '{PRODUCT_NAME}'"
            )
        if abs((v.quantity or 0.0) - DEMAND_QTY) > 1e-6:
            failures.append(
                f"Adjustment line quantity is {v.quantity}, "
                f"expected {DEMAND_QTY}"
            )
        if abs((v.additional_landed_cost or 0.0) - COST_AMOUNT) > 1e-6:
            failures.append(
                f"Adjustment line additional_landed_cost is "
                f"{v.additional_landed_cost}, expected {COST_AMOUNT} "
                "(45 EUR allocated entirely to the single move)"
            )

    # Amount total.
    if abs((lc.amount_total or 0.0) - COST_AMOUNT) > 1e-6:
        failures.append(
            f"Landed cost amount_total is {lc.amount_total}, "
            f"expected {COST_AMOUNT}"
        )

    # Receipt move sanity — the single Bench Import Item move on the
    # validated receipt should still exist with the right qty.
    item_moves = receipt.move_ids.filtered(
        lambda m: m.product_id.id == item.id
    )
    if len(item_moves) != 1:
        failures.append(
            f"Receipt has {len(item_moves)} Bench Import Item moves, "
            "expected 1"
        )
    elif abs((item_moves[0].quantity or 0.0) - DEMAND_QTY) > 1e-6:
        failures.append(
            f"Receipt move quantity is {item_moves[0].quantity}, "
            f"expected {DEMAND_QTY} (agent must not touch the receipt)"
        )

    return failures
