"""Postcondition checks for sale_purchase.dropship_so_to_po_chain_validate."""


SO_REF = "S-BENCH-DS-001"
VENDOR_NAME = "Bench Dropship Supplier"
CUSTOMER_NAME = "Bench Dropship Buyer"
PRODUCT_NAME = "Bench Dropship Gadget"
QTY = 5.0


def check(env):
    failures = []

    # --- 1. SO must exist and be confirmed (state='sale') ---
    so = env["sale.order"].search(
        [("client_order_ref", "=", SO_REF)], limit=1
    )
    if not so:
        return [f"Sales order {SO_REF!r} not found"]

    if so.state != "sale":
        failures.append(f"SO state is {so.state!r}, expected 'sale'")

    # SO line delivered qty must equal 5
    line = so.order_line.filtered(lambda l: l.product_id.name == PRODUCT_NAME)
    if not line:
        failures.append(f"SO line for {PRODUCT_NAME!r} not found")
    else:
        line = line[0]
        delivered = getattr(line, "qty_delivered", 0.0) or 0.0
        if abs(delivered - QTY) > 0.01:
            failures.append(
                f"SO line qty_delivered for {PRODUCT_NAME!r} is "
                f"{delivered}, expected {QTY}"
            )

    # --- 2. Auto-generated PO for vendor must be confirmed ---
    # The PO's origin is the SO's internal name (e.g. S00001), not the
    # client_order_ref. Look up via vendor + origin = so.name.
    vendor = env["res.partner"].search([("name", "=", VENDOR_NAME)], limit=1)
    if not vendor:
        failures.append(f"Vendor {VENDOR_NAME!r} not found")
        return failures

    po = env["purchase.order"].search([
        ("partner_id", "=", vendor.id),
        ("origin", "=", so.name),
    ], limit=1)
    if not po:
        # Fallback: any PO for this vendor whose origin contains the SO name
        po = env["purchase.order"].search([
            ("partner_id", "=", vendor.id),
            ("origin", "ilike", so.name),
        ], limit=1)
    if not po:
        failures.append(
            f"Auto-generated PO for vendor {VENDOR_NAME!r} (origin {so.name!r}) "
            "not found"
        )
    else:
        if po.state != "purchase":
            failures.append(
                f"PO state is {po.state!r}, expected 'purchase'"
            )

    # --- 3. Dropship picking must be done with qty=5 ---
    # Dropship pickings are linked to the SO via SO.picking_ids and have
    # picking_type code 'dropship'.
    pickings = so.picking_ids
    if not pickings:
        failures.append("No pickings linked to the SO")
    else:
        dropship_pickings = pickings.filtered(
            lambda p: p.picking_type_id.code == "dropship"
        )
        if not dropship_pickings:
            failures.append(
                "No dropship picking found on SO — agent may have used a "
                "regular customer delivery instead"
            )
        else:
            done_pickings = dropship_pickings.filtered(
                lambda p: p.state == "done"
            )
            if not done_pickings:
                states = ", ".join(
                    sorted({p.state for p in dropship_pickings})
                )
                failures.append(
                    f"No dropship picking is in state 'done' "
                    f"(found states: {states})"
                )
            else:
                # Verify the done picking moved 5 units of the dropship product
                picked = done_pickings[0]
                product_moves = picked.move_ids.filtered(
                    lambda m: m.product_id.name == PRODUCT_NAME
                )
                if not product_moves:
                    failures.append(
                        f"Done dropship picking has no move for {PRODUCT_NAME!r}"
                    )
                else:
                    move = product_moves[0]
                    qty = getattr(move, "quantity", None)
                    if qty is None:
                        qty = getattr(move, "quantity_done", 0.0) or 0.0
                    if abs(qty - QTY) > 0.01:
                        failures.append(
                            f"Dropship picking move quantity is {qty}, "
                            f"expected {QTY}"
                        )

    return failures
