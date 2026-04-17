"""Postcondition checks for stock.validate_delivery_shipment.

Validates:
1. Target delivery BENCH-DEL-01 is in state 'done'.
2. The two move lines have quantity_done (or quantity) equal to 12 and 5.
3. No backorder transfer was created from BENCH-DEL-01.
4. The distractor delivery BENCH-DEL-OTHER is still in 'assigned' state.
"""


def check(env):
    failures = []

    target = env["stock.picking"].search(
        [("origin", "=", "BENCH-DEL-01")], limit=1
    )
    if not target:
        return ["Target delivery 'BENCH-DEL-01' not found"]

    if target.state != "done":
        failures.append(
            f"Target delivery state is '{target.state}', expected 'done'"
        )

    moves = target.move_ids
    if len(moves) != 2:
        failures.append(
            f"Target delivery has {len(moves)} moves, expected 2"
        )
        return failures

    steel = moves.filtered(lambda m: m.product_id.name == "Steel Bracket 12\"")
    wire = moves.filtered(lambda m: m.product_id.name == "Copper Wire 100m")

    # Quantity attribute on stock.move in Odoo 19: `quantity` (validated qty)
    if not steel:
        failures.append("Steel Bracket 12\" move is missing on target delivery")
    else:
        delivered = getattr(steel, "quantity", None)
        if delivered is None:
            delivered = steel.quantity_done
        if abs(delivered - 12) > 0.001:
            failures.append(
                f"Steel Bracket 12\" delivered qty is {delivered}, expected 12"
            )
    if not wire:
        failures.append("Copper Wire 100m move is missing on target delivery")
    else:
        delivered = getattr(wire, "quantity", None)
        if delivered is None:
            delivered = wire.quantity_done
        if abs(delivered - 5) > 0.001:
            failures.append(
                f"Copper Wire 100m delivered qty is {delivered}, expected 5"
            )

    backorders = env["stock.picking"].search([
        ("backorder_id", "=", target.id),
        ("state", "!=", "cancel"),
    ])
    if backorders:
        failures.append(
            f"Unexpected backorder(s) created: {backorders.mapped('name')}"
        )

    distractor = env["stock.picking"].search(
        [("origin", "=", "BENCH-DEL-OTHER")], limit=1
    )
    if not distractor:
        failures.append("Distractor delivery 'BENCH-DEL-OTHER' missing")
    elif distractor.state == "done":
        failures.append(
            "Distractor delivery 'BENCH-DEL-OTHER' was validated — must stay pending"
        )

    return failures
