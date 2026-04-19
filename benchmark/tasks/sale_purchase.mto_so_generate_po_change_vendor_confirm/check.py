"""Postcondition checks for sale_purchase.mto_so_generate_po_change_vendor_confirm.

Validates:
1. SO S-BENCH-MTO-001 exists, state='sale', single line qty=8 @ 150.00.
2. An auto-generated PO with origin referencing the SO exists, has vendor
   Orion Component Works, and state='purchase'.
3. No active (non-cancelled) PO with vendor Alpha Precision Parts linked
   to this SO remains — i.e. the agent swapped the vendor on the existing
   RFQ rather than creating a new PO.
"""


SO_REF = "S-BENCH-MTO-001"
CUSTOMER_NAME = "Harbor MTO Buyer"
PRODUCT_NAME = "Harbor MTO Gadget"
VENDOR_PRIMARY = "Alpha Precision Parts"
VENDOR_ALT = "Orion Component Works"
QTY = 8
PRICE_UNIT = 150.0


def check(env):
    failures = []

    so = env["sale.order"].search(
        [("client_order_ref", "=", SO_REF)], limit=1
    )
    if not so:
        return [f"Sales order {SO_REF!r} not found"]

    if so.state != "sale":
        failures.append(f"SO state is {so.state!r}, expected 'sale'")

    # Line intact
    lines = so.order_line
    if len(lines) != 1:
        failures.append(f"SO has {len(lines)} lines, expected 1")
    else:
        line = lines[0]
        if line.product_id.name != PRODUCT_NAME:
            failures.append(
                f"SO line product is {line.product_id.name!r}, "
                f"expected {PRODUCT_NAME!r}"
            )
        if abs(line.product_uom_qty - QTY) > 0.01:
            failures.append(
                f"SO line qty is {line.product_uom_qty}, expected {QTY}"
            )
        if abs(line.price_unit - PRICE_UNIT) > 0.01:
            failures.append(
                f"SO line price_unit is {line.price_unit}, expected {PRICE_UNIT}"
            )

    # Customer unchanged
    if so.partner_id.name != CUSTOMER_NAME:
        failures.append(
            f"SO customer is {so.partner_id.name!r}, expected {CUSTOMER_NAME!r}"
        )

    vendor_primary = env["res.partner"].search(
        [("name", "=", VENDOR_PRIMARY)], limit=1
    )
    vendor_alt = env["res.partner"].search(
        [("name", "=", VENDOR_ALT)], limit=1
    )
    if not vendor_primary or not vendor_alt:
        failures.append("Seed vendors not found")
        return failures

    # Find purchase orders linked to this SO. MTO sets origin to the
    # generated SO internal name (e.g. S00001). If the agent somehow
    # carried the client_order_ref into the PO origin (shouldn't happen),
    # catch that too.
    linked_pos = env["purchase.order"].search([
        "|", ("origin", "=", so.name),
             ("origin", "=", SO_REF),
    ])
    if not linked_pos:
        failures.append(
            f"No purchase order with origin {so.name!r} (or {SO_REF!r}) found"
        )
        return failures

    # Among linked POs: there must be exactly one non-cancelled, and it
    # must be the confirmed alternative-vendor PO.
    active_pos = linked_pos.filtered(lambda p: p.state != "cancel")
    if not active_pos:
        failures.append(
            "All linked POs are cancelled — agent should have swapped the vendor, "
            "not cancelled the RFQ"
        )
        return failures

    # The final active PO must be for Orion Component Works.
    alt_pos = active_pos.filtered(lambda p: p.partner_id.id == vendor_alt.id)
    if not alt_pos:
        vendors_seen = ", ".join(sorted({p.partner_id.name for p in active_pos}))
        failures.append(
            f"No active linked PO has vendor {VENDOR_ALT!r}; saw vendors: "
            f"{vendors_seen}"
        )
        return failures

    # The Orion PO must be confirmed.
    confirmed = alt_pos.filtered(lambda p: p.state == "purchase")
    if not confirmed:
        states = ", ".join(sorted({p.state for p in alt_pos}))
        failures.append(
            f"PO for {VENDOR_ALT!r} is not confirmed (states: {states}); "
            f"expected 'purchase'"
        )

    # No active PO should reference the original vendor Alpha Precision
    # Parts — otherwise the agent created a new PO instead of editing.
    primary_active = active_pos.filtered(
        lambda p: p.partner_id.id == vendor_primary.id
    )
    if primary_active:
        failures.append(
            f"Found {len(primary_active)} active PO(s) for {VENDOR_PRIMARY!r} "
            "linked to this SO — agent must swap the existing RFQ rather than "
            "creating a second PO"
        )

    # Sanity: exactly one active linked PO overall.
    if len(active_pos) != 1:
        failures.append(
            f"Expected exactly 1 active PO linked to SO {so.name!r}, "
            f"found {len(active_pos)}"
        )

    # Line on the final PO: same product + qty.
    final_po = confirmed[:1] if confirmed else alt_pos[:1]
    po_lines = final_po.order_line
    if len(po_lines) != 1:
        failures.append(
            f"Final PO has {len(po_lines)} lines, expected 1"
        )
    else:
        pol = po_lines[0]
        if pol.product_id.name != PRODUCT_NAME:
            failures.append(
                f"PO line product is {pol.product_id.name!r}, "
                f"expected {PRODUCT_NAME!r}"
            )
        if abs(pol.product_qty - QTY) > 0.01:
            failures.append(
                f"PO line qty is {pol.product_qty}, expected {QTY}"
            )

    return failures
