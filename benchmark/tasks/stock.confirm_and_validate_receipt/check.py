"""Postcondition checks for stock.confirm_and_validate_receipt.

Validates:
1. Receipt BENCH-RCV-01 exists and is done
2. Both product lines have correct received quantities
"""

RECEIPT_REF = "BENCH-RCV-01"


def check(env):
    failures = []

    picking = env["stock.picking"].search([
        ("origin", "=", RECEIPT_REF),
    ], limit=1)

    if not picking:
        return [f"Receipt with origin '{RECEIPT_REF}' not found"]

    # Check state
    if picking.state != "done":
        failures.append(f"Receipt state is '{picking.state}', expected 'done'")

    # Check move lines
    moves = picking.move_ids
    if len(moves) != 2:
        failures.append(f"Expected 2 stock moves, found {len(moves)}")
        return failures

    steel_move = moves.filtered(
        lambda m: "Steel Bracket" in m.product_id.name
    )
    copper_move = moves.filtered(
        lambda m: "Copper Wire" in m.product_id.name
    )

    if not steel_move:
        failures.append("Steel Bracket 12\" move not found")
    else:
        if steel_move.quantity != 20.0:
            failures.append(
                f"Steel Bracket done qty is {steel_move.quantity}, expected 20"
            )

    if not copper_move:
        failures.append("Copper Wire 100m move not found")
    else:
        if copper_move.quantity != 10.0:
            failures.append(
                f"Copper Wire done qty is {copper_move.quantity}, expected 10"
            )

    return failures
