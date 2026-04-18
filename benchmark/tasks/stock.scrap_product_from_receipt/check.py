"""Postcondition checks for stock.scrap_product_from_receipt.

Validates:
1. Exactly one stock.scrap exists for Bench Scrap Product.
2. That scrap is in state 'done' with scrap_qty == 2.
3. The scrap is linked to the seeded receipt BENCH-RCV-SCRAP-01.
4. The original receipt is still in 'done' state with 10 received units.
"""

PRODUCT_NAME = "Bench Scrap Product"
RECEIPT_REF = "BENCH-RCV-SCRAP-01"


def check(env):
    failures = []

    products = env["product.product"].search([("name", "=", PRODUCT_NAME)])
    if not products:
        return [f"Product '{PRODUCT_NAME}' is missing"]
    product = products[0]

    picking = env["stock.picking"].search(
        [("origin", "=", RECEIPT_REF)], limit=1
    )
    if not picking:
        return [f"Seeded receipt '{RECEIPT_REF}' is missing (did the agent delete it?)"]

    # Original receipt must still be done with 10 units received
    if picking.state != "done":
        failures.append(
            f"Seeded receipt state is '{picking.state}', expected 'done' "
            f"(agent must not cancel or reset the receipt)"
        )
    original_moves = picking.move_ids.filtered(
        lambda m: m.product_id.id == product.id and not m.scrap_id
    )
    if not original_moves:
        failures.append("Original receipt is missing the Bench Scrap Product line")
    else:
        total_received = sum(original_moves.mapped("quantity"))
        if abs(total_received - 10.0) > 0.01:
            failures.append(
                f"Original receipt received qty is {total_received}, expected 10 "
                f"(agent must not modify the original receipt)"
            )

    scraps = env["stock.scrap"].search([("product_id", "=", product.id)])
    if len(scraps) == 0:
        failures.append(
            f"No stock.scrap exists for '{PRODUCT_NAME}' — agent did not create a scrap"
        )
        return failures
    if len(scraps) != 1:
        failures.append(
            f"Expected exactly 1 stock.scrap for '{PRODUCT_NAME}', found {len(scraps)}"
        )

    scrap = scraps[0]
    if scrap.state != "done":
        failures.append(
            f"Scrap state is '{scrap.state}', expected 'done' "
            f"(agent did not click Validate on the scrap)"
        )
    if abs(scrap.scrap_qty - 2.0) > 0.01:
        failures.append(
            f"Scrap quantity is {scrap.scrap_qty}, expected 2"
        )
    if not scrap.picking_id:
        failures.append(
            f"Scrap is not linked to any picking — expected link to "
            f"receipt '{RECEIPT_REF}' (agent must scrap from the receipt)"
        )
    elif scrap.picking_id.id != picking.id:
        failures.append(
            f"Scrap is linked to picking '{scrap.picking_id.name}' "
            f"(origin='{scrap.picking_id.origin}'), expected origin "
            f"'{RECEIPT_REF}'"
        )

    return failures
