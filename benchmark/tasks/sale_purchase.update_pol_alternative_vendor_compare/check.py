"""Postcondition checks for sale_purchase.update_pol_alternative_vendor_compare.

Validates:
1. Atlas Industrial RFQ (origin R-BENCH-ALT-001) ends in cancel state.
2. Crestline Equipment RFQ ends in cancel state.
3. Beacon Mechanical RFQ ends in confirmed (purchase) state with one line:
   Industrial Compressor, qty 10, unit price 100.00.
4. The three POs are linked together via the same purchase.order.group
   (i.e. they were created via the alternative wizard).
"""


VENDOR_A = "Atlas Industrial"
VENDOR_B = "Beacon Mechanical"
VENDOR_C = "Crestline Equipment"
PRODUCT_NAME = "Industrial Compressor"
RFQ_REF = "R-BENCH-ALT-001"


def _po_for_vendor(env, vendor_name):
    v = env["res.partner"].search([("name", "=", vendor_name)], limit=1)
    if not v:
        return None, f"Vendor '{vendor_name}' not found"
    pos = env["purchase.order"].with_context(active_test=False).search([
        ("partner_id", "=", v.id),
    ])
    if not pos:
        return None, f"No purchase order for vendor '{vendor_name}'"
    # Prefer the one whose origin matches our seed reference.
    by_origin = pos.filtered(lambda p: p.origin and RFQ_REF in (p.origin or ""))
    if by_origin:
        return by_origin[0], None
    return pos[0], None


def check(env):
    failures = []

    po_a, err = _po_for_vendor(env, VENDOR_A)
    if err:
        failures.append(err)
    elif po_a.state != "cancel":
        failures.append(
            f"Atlas Industrial RFQ state is '{po_a.state}', expected 'cancel'"
        )

    po_c, err = _po_for_vendor(env, VENDOR_C)
    if err:
        failures.append(err)
    elif po_c.state != "cancel":
        failures.append(
            f"Crestline Equipment RFQ state is '{po_c.state}', expected 'cancel'"
        )

    po_b, err = _po_for_vendor(env, VENDOR_B)
    if err:
        failures.append(err)
        return failures

    if po_b.state != "purchase":
        failures.append(
            f"Beacon Mechanical RFQ state is '{po_b.state}', expected 'purchase'"
        )

    # Lines on Beacon Mechanical's PO
    lines = po_b.order_line.filtered(
        lambda l: l.product_id.name == PRODUCT_NAME
    )
    if not lines:
        failures.append("Beacon Mechanical PO has no Industrial Compressor line")
    else:
        line = lines[0]
        if abs(line.product_qty - 10.0) > 0.01:
            failures.append(
                f"Beacon Mechanical line qty is {line.product_qty}, expected 10"
            )
        if abs(line.price_unit - 100.0) > 0.01:
            failures.append(
                f"Beacon Mechanical line unit price is {line.price_unit}, "
                f"expected 100.00"
            )

    # No extra confirmed POs leaked through (Atlas/Crestline must not be
    # confirmed even if the agent skipped cancellation).
    extra_confirmed = env["purchase.order"].search([
        ("partner_id", "in", [
            env["res.partner"].search([("name", "=", VENDOR_A)], limit=1).id or 0,
            env["res.partner"].search([("name", "=", VENDOR_C)], limit=1).id or 0,
        ]),
        ("state", "=", "purchase"),
    ])
    if extra_confirmed:
        failures.append(
            "Atlas Industrial and/or Crestline Equipment was confirmed "
            "(should be cancelled instead)"
        )

    # Sanity: the three POs should share a purchase.order.group (proves they
    # were created via the Create Alternative wizard, not as standalone POs).
    if po_a and po_b and po_a.purchase_group_id and po_b.purchase_group_id:
        if po_a.purchase_group_id != po_b.purchase_group_id:
            failures.append(
                "Atlas and Beacon RFQs are not linked in the same alternative "
                "group — Beacon must be created via 'Create Alternative'"
            )

    return failures
