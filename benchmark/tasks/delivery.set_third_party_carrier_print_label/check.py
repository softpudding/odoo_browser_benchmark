"""Postcondition checks for delivery.set_third_party_carrier_print_label.

Validates:
1. A 'Bench Express' fixed-price carrier exists with fixed_price 12.0.
2. The delivery picking sourced from S-BENCH-DLV-002 has the carrier
   set, has a non-empty carrier_tracking_ref equal to 'BX-TRACK-002',
   and is in state 'done'.
3. The original move quantity (3) was actually delivered.
"""


def check(env):
    failures = []

    carrier = env["delivery.carrier"].search(
        [("name", "=", "Bench Express")], limit=1
    )
    if not carrier:
        return ["Delivery method 'Bench Express' not found"]

    if carrier.delivery_type != "fixed":
        failures.append(
            f"Carrier delivery_type is '{carrier.delivery_type}', expected 'fixed'"
        )
    if abs(carrier.fixed_price - 12.0) > 0.0001:
        failures.append(
            f"Carrier fixed_price is {carrier.fixed_price}, expected 12.00"
        )

    so = env["sale.order"].search(
        [("client_order_ref", "=", "S-BENCH-DLV-002")], limit=1
    )
    if not so:
        return failures + [
            "Sale order with customer reference 'S-BENCH-DLV-002' not found"
        ]

    pickings = so.picking_ids.filtered(lambda p: p.picking_type_code == "outgoing")
    if not pickings:
        return failures + ["No outgoing delivery picking found for S-BENCH-DLV-002"]

    target = pickings[0]
    if target.state != "done":
        failures.append(
            f"Delivery picking state is '{target.state}', expected 'done'"
        )
    if target.carrier_id != carrier:
        failures.append(
            f"Delivery picking carrier is '{target.carrier_id.name or 'unset'}', "
            "expected 'Bench Express'"
        )
    expected_ref = "BX-TRACK-002"
    if not target.carrier_tracking_ref:
        failures.append(
            "Delivery picking carrier_tracking_ref is empty, expected 'BX-TRACK-002'"
        )
    elif expected_ref not in target.carrier_tracking_ref:
        failures.append(
            f"Delivery picking carrier_tracking_ref is "
            f"'{target.carrier_tracking_ref}', expected to contain '{expected_ref}'"
        )

    moves = target.move_ids
    if len(moves) != 1:
        failures.append(
            f"Delivery picking has {len(moves)} moves, expected 1"
        )
    else:
        move = moves[0]
        delivered = getattr(move, "quantity", None)
        if delivered is None:
            delivered = getattr(move, "quantity_done", 0.0)
        if abs(delivered - 3.0) > 0.001:
            failures.append(
                f"Bench Express Crate delivered qty is {delivered}, expected 3"
            )

    return failures
