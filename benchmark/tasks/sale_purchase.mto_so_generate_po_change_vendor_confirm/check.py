"""Postcondition checks for sale_purchase.mto_so_generate_po_change_vendor_confirm.

Validates:
1. SO S-BENCH-MTO-001 exists, is confirmed (state='sale'), and still has
   exactly ONE linked purchase order via the MTO chain (origin=SO.name).
2. That linked PO:
    - partner_id = Brook Trading Ltd  (NOT Acme Supply Co)
    - state      = 'purchase'         (Confirmed)
    - order_line = 1 line: Bench MTO Widget qty 5 @ 40.00
3. No extra PO exists for Acme Supply Co connected to this SO (the agent
   must have edited the generated RFQ, not duplicated it).

Note: For MTO+Buy (non-dropship) the generated purchase.order.line does
NOT carry sale_line_id (that field is only populated for dropship).  The
canonical SO<->PO link is ``purchase.order.origin == sale.order.name``.
"""


VENDOR_A = "Acme Supply Co"
VENDOR_B = "Brook Trading Ltd"
CUSTOMER_NAME = "Bench MTO Customer"
PRODUCT_NAME = "Bench MTO Widget"
SO_NAME = "S-BENCH-MTO-001"
QTY = 5
PRICE_B = 40.0


def check(env):
    failures = []

    so = env["sale.order"].with_context(active_test=False).search(
        [("name", "=", SO_NAME)], limit=1
    )
    if not so:
        return [f"Sale order {SO_NAME} not found"]

    if so.state != "sale":
        failures.append(
            f"SO state is '{so.state}', expected 'sale'"
        )

    # Collect POs linked to this SO via origin (MTO+Buy chain).
    linked_pos = env["purchase.order"].with_context(active_test=False).search([
        ("origin", "=", so.name),
    ])
    linked_pos = linked_pos.sudo()

    if len(linked_pos) == 0:
        return failures + [
            "No purchase order linked to SO via MTO (agent likely created a "
            "standalone PO; the SO<->PO link is broken)"
        ]

    if len(linked_pos) > 1:
        partners = ", ".join(linked_pos.mapped("partner_id.name"))
        failures.append(
            f"Expected exactly 1 PO linked to SO, got {len(linked_pos)} "
            f"(vendors: {partners})"
        )

    # Find the "target" PO: the one for Brook Trading Ltd, preferably.
    po_target = linked_pos.filtered(lambda p: p.partner_id.name == VENDOR_B)
    if not po_target:
        partners = ", ".join(linked_pos.mapped("partner_id.name"))
        failures.append(
            f"Linked PO vendor is not '{VENDOR_B}' (found: {partners}); "
            "agent must switch the auto-generated RFQ's vendor"
        )
        po_target = linked_pos[:1]
    else:
        po_target = po_target[0]

    if po_target.state != "purchase":
        failures.append(
            f"Linked PO state is '{po_target.state}', expected 'purchase'"
        )

    widget_lines = po_target.order_line.filtered(
        lambda l: l.product_id.name == PRODUCT_NAME
    )
    if len(widget_lines) != 1:
        failures.append(
            f"Expected exactly 1 {PRODUCT_NAME} line on the linked PO, "
            f"got {len(widget_lines)}"
        )
    else:
        line = widget_lines
        if abs(line.product_qty - QTY) > 0.01:
            failures.append(
                f"PO line qty is {line.product_qty}, expected {QTY}"
            )
        if abs(line.price_unit - PRICE_B) > 0.01:
            failures.append(
                f"PO line unit price is {line.price_unit}, expected {PRICE_B}"
            )

    # No leaked Acme PO hanging off the same SO
    acme_pos = linked_pos.filtered(lambda p: p.partner_id.name == VENDOR_A)
    acme_active = acme_pos.filtered(lambda p: p.state not in ("cancel",))
    if acme_active:
        failures.append(
            f"Found {len(acme_active)} non-cancelled PO(s) for '{VENDOR_A}' "
            f"still linked to the SO (agent should have changed the vendor "
            f"on the existing RFQ, not created a second PO)"
        )

    return failures
