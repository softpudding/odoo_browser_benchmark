"""Postcondition checks for purchase.create_rfq_receive_invoice_3way_match.

Validates all three legs of the 3-way match:
  1. A purchase.order exists for vendor 'Bench Supply Co' with state
     'purchase', exactly 2 lines in the right order with correct qty and
     price, and qty_received 7 (A) / 5 (B).
  2. The original auto-generated receipt is in state 'done'; a backorder
     picking exists with 3 remaining Item A units (state in
     confirmed/assigned/waiting).
  3. Exactly one posted account.move with move_type='in_invoice',
     ref='BSC-BILL-3WM', linked to that PO via invoice_line_ids
     .purchase_line_id, with matching qty per line.
  4. Distractor RFQ 'R-BENCH-FILLER-001' must still be draft, untouched.
"""


VENDOR_NAME = "Bench Supply Co"
DISTRACTOR_VENDOR = "Bench Filler Vendor"
PRODUCT_A = "Bench PO Item A"
PRODUCT_B = "Bench PO Item B"
PRICE_A = 20.0
PRICE_B = 40.0
DEMAND_A = 10.0
DEMAND_B = 5.0
RECEIVED_A = 7.0
RECEIVED_B = 5.0
BACKORDER_A = 3.0
BILL_REF = "BSC-BILL-3WM"
DISTRACTOR_REF = "R-BENCH-FILLER-001"


def _close(a, b, tol=1e-6):
    return abs((a or 0.0) - (b or 0.0)) <= tol


def check(env):
    failures = []

    vendor = env["res.partner"].search([("name", "=", VENDOR_NAME)], limit=1)
    if not vendor:
        return [f"Vendor '{VENDOR_NAME}' not found"]

    prod_a = env["product.product"].search([("name", "=", PRODUCT_A)], limit=1)
    prod_b = env["product.product"].search([("name", "=", PRODUCT_B)], limit=1)
    if not prod_a or not prod_b:
        return failures + [
            f"Products {PRODUCT_A!r}/{PRODUCT_B!r} missing (seed not applied?)"
        ]

    # ------------------------------------------------------------------
    # 1. Purchase order
    # ------------------------------------------------------------------
    pos = env["purchase.order"].search([
        ("partner_id", "=", vendor.id),
        ("state", "in", ("purchase", "done")),
    ])
    if not pos:
        return failures + [
            f"No confirmed PO found for vendor '{VENDOR_NAME}' — agent did "
            f"not create+confirm an RFQ"
        ]
    if len(pos) > 1:
        failures.append(
            f"Expected exactly 1 confirmed PO for '{VENDOR_NAME}', found "
            f"{len(pos)}: {pos.mapped('name')}"
        )
    po = pos[:1]

    if po.state != "purchase":
        failures.append(f"PO state is '{po.state}', expected 'purchase'")

    # Lines — must be exactly 2, products A then B, qty 10 / 5, price
    # 20 / 40, qty_received 7 / 5.
    lines = po.order_line.sorted("id")
    if len(lines) != 2:
        failures.append(
            f"PO has {len(lines)} order lines, expected exactly 2 "
            f"(agent may have left a phantom empty third line)"
        )
    else:
        want = [
            (PRODUCT_A, DEMAND_A, PRICE_A, RECEIVED_A),
            (PRODUCT_B, DEMAND_B, PRICE_B, RECEIVED_B),
        ]
        for i, (pname, qty, price, qty_recv) in enumerate(want):
            ln = lines[i]
            if ln.product_id.name != pname:
                failures.append(
                    f"PO line {i + 1} product is '{ln.product_id.name}', "
                    f"expected '{pname}'"
                )
            if not _close(ln.product_qty, qty):
                failures.append(
                    f"PO line {i + 1} ({pname}) qty is {ln.product_qty}, "
                    f"expected {qty}"
                )
            if not _close(ln.price_unit, price):
                failures.append(
                    f"PO line {i + 1} ({pname}) price_unit is "
                    f"{ln.price_unit}, expected {price}"
                )
            if not _close(ln.qty_received, qty_recv):
                failures.append(
                    f"PO line {i + 1} ({pname}) qty_received is "
                    f"{ln.qty_received}, expected {qty_recv}"
                )

    # ------------------------------------------------------------------
    # 2. Pickings — original done + backorder with 3 remaining A
    # ------------------------------------------------------------------
    originals = po.picking_ids.filtered(lambda p: not p.backorder_id)
    if not originals:
        failures.append(
            "No original (non-backorder) receipt found for the PO"
        )
    else:
        if len(originals) > 1:
            failures.append(
                f"Expected exactly 1 original receipt, found "
                f"{len(originals)}: {originals.mapped('name')}"
            )
        orig = originals[:1]
        if orig.state != "done":
            failures.append(
                f"Original receipt state is '{orig.state}', expected 'done' "
                f"— agent likely did not Validate"
            )

        # Original move line for Item A should show qty=7 and for B qty=5
        for product, received in ((prod_a, RECEIVED_A), (prod_b, RECEIVED_B)):
            moves = orig.move_ids.filtered(
                lambda m, p=product: m.product_id.id == p.id and not m.scrap_id
            )
            if len(moves) != 1:
                failures.append(
                    f"Original receipt has {len(moves)} moves for "
                    f"{product.name}, expected 1"
                )
            else:
                if not _close(moves.quantity, received):
                    failures.append(
                        f"Original receipt {product.name} Done qty is "
                        f"{moves.quantity}, expected {received}"
                    )

        # Backorder picking
        backorders = po.picking_ids.filtered(
            lambda p, o=orig: p.backorder_id.id == o.id
        )
        if not backorders:
            failures.append(
                "No backorder receipt found — agent likely clicked "
                "'No Backorder' instead of 'Create Backorder'"
            )
        else:
            if len(backorders) > 1:
                failures.append(
                    f"Expected exactly 1 backorder, found "
                    f"{len(backorders)}: {backorders.mapped('name')}"
                )
            bo = backorders[:1]
            if bo.state in ("done", "cancel"):
                failures.append(
                    f"Backorder state is '{bo.state}', expected a pending "
                    f"state (confirmed / assigned / waiting)"
                )
            bo_a_moves = bo.move_ids.filtered(
                lambda m: m.product_id.id == prod_a.id and not m.scrap_id
            )
            if len(bo_a_moves) != 1:
                failures.append(
                    f"Backorder has {len(bo_a_moves)} Item A moves, "
                    f"expected 1"
                )
            elif not _close(bo_a_moves.product_uom_qty, BACKORDER_A):
                failures.append(
                    f"Backorder Item A demand is "
                    f"{bo_a_moves.product_uom_qty}, expected {BACKORDER_A}"
                )

    # ------------------------------------------------------------------
    # 3. Vendor bill posted, referencing PO
    # ------------------------------------------------------------------
    bills = env["account.move"].search([
        ("move_type", "=", "in_invoice"),
        ("partner_id", "=", vendor.id),
    ])
    if not bills:
        return failures + [
            "No vendor bill (account.move move_type='in_invoice') found "
            "for the vendor — agent never clicked Create Bill"
        ]

    # Prefer the one with our ref; else the most recent draft/posted.
    target_bill = bills.filtered(lambda b: b.ref == BILL_REF)
    if not target_bill:
        failures.append(
            f"No vendor bill with Bill Reference '{BILL_REF}' found — "
            f"agent may have typed the wrong ref or skipped it"
        )
        target_bill = bills
    bill = target_bill[:1]

    if bill.state != "posted":
        failures.append(
            f"Vendor bill state is '{bill.state}', expected 'posted' — "
            f"agent likely did not click Confirm on the bill"
        )

    # Must be linked to our PO.
    linked_pos = bill.invoice_line_ids.mapped("purchase_line_id.order_id")
    if po not in linked_pos:
        failures.append(
            f"Vendor bill is not linked to PO '{po.name}' (links: "
            f"{linked_pos.mapped('name')}). Agent may have created a "
            f"standalone bill instead of clicking Create Bill on the PO."
        )

    # Bill line qty must match received qty (3-way match enforcement).
    bill_lines = bill.invoice_line_ids.filtered(
        lambda l: l.display_type is False or l.display_type == "product"
    )
    # fallback to product_type rows
    if not bill_lines:
        bill_lines = bill.invoice_line_ids
    for product, received in ((prod_a, RECEIVED_A), (prod_b, RECEIVED_B)):
        prod_line = bill_lines.filtered(
            lambda l, p=product: l.product_id.id == p.id
        )
        if not prod_line:
            failures.append(
                f"Vendor bill has no line for {product.name}"
            )
        elif not _close(prod_line[:1].quantity, received):
            failures.append(
                f"Vendor bill {product.name} quantity is "
                f"{prod_line[:1].quantity}, expected {received} (must "
                f"match received qty)"
            )

    # ------------------------------------------------------------------
    # 4. Distractor RFQ must still be draft.
    # ------------------------------------------------------------------
    distractor = env["purchase.order"].search([
        ("partner_ref", "=", DISTRACTOR_REF),
    ], limit=1)
    if distractor and distractor.state != "draft":
        failures.append(
            f"Distractor RFQ '{DISTRACTOR_REF}' state is "
            f"'{distractor.state}', expected 'draft' — agent wrongly "
            f"touched it"
        )

    return failures
