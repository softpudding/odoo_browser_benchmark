"""Postcondition checks for purchase.confirm_rfq_receive_full_three_way_match.

Validates three things:
  1. The seeded PO (partner_ref='BENCH-RFQ-3WAY-2') is confirmed
     (state='purchase'), has both lines unchanged, qty_received matches
     ordered, and invoice_status='to invoice' (3-way match READY).
  2. The auto-generated stock.picking is in state='done' with the full
     demand received (8 and 12).
  3. NO vendor bill (account.move with move_type='in_invoice') has been
     created for the vendor — the task stops at receipt validation.
"""


VENDOR_NAME = "Bench Supplier Inc"
RFQ_REF = "BENCH-RFQ-3WAY-2"
PRODUCT_A = "Bench 3WM Bracket"
PRODUCT_B = "Bench 3WM Fastener Kit"
PRICE_A = 25.0
PRICE_B = 5.0
QTY_A = 8.0
QTY_B = 12.0


def _close(a, b, tol=1e-6):
    return abs((a or 0.0) - (b or 0.0)) <= tol


def check(env):
    failures = []

    vendor = env["res.partner"].search([("name", "=", VENDOR_NAME)], limit=1)
    if not vendor:
        return [f"Vendor '{VENDOR_NAME}' not found"]

    po = env["purchase.order"].search([
        ("partner_id", "=", vendor.id),
        ("partner_ref", "=", RFQ_REF),
    ], limit=1)
    if not po:
        return [
            f"Target RFQ with partner_ref='{RFQ_REF}' not found for vendor "
            f"'{VENDOR_NAME}' (seed not applied or agent modified ref)"
        ]

    # --- PO state + invoice_status -------------------------------------
    if po.state != "purchase":
        failures.append(
            f"PO state is '{po.state}', expected 'purchase' — agent likely "
            f"did not click Confirm Order"
        )

    if po.invoice_status != "to invoice":
        failures.append(
            f"PO invoice_status is '{po.invoice_status}', expected "
            f"'to invoice' (3-way match READY). 'no' = receipt not "
            f"validated; 'invoiced' = a bill was created (forbidden)."
        )

    # --- PO lines unchanged + qty_received matches demand --------------
    lines = po.order_line.sorted("id")
    if len(lines) != 2:
        failures.append(
            f"PO has {len(lines)} order lines, expected 2 (agent may "
            f"have added or removed lines)"
        )
    else:
        want = [
            (PRODUCT_A, QTY_A, PRICE_A),
            (PRODUCT_B, QTY_B, PRICE_B),
        ]
        for i, (pname, qty, price) in enumerate(want):
            ln = lines[i]
            if ln.product_id.name != pname:
                failures.append(
                    f"PO line {i + 1} product is '{ln.product_id.name}', "
                    f"expected '{pname}'"
                )
            if not _close(ln.product_qty, qty):
                failures.append(
                    f"PO line {i + 1} ({pname}) product_qty is "
                    f"{ln.product_qty}, expected {qty} (ordered qty must "
                    f"not change)"
                )
            if not _close(ln.price_unit, price):
                failures.append(
                    f"PO line {i + 1} ({pname}) price_unit is "
                    f"{ln.price_unit}, expected {price}"
                )
            if not _close(ln.qty_received, qty):
                failures.append(
                    f"PO line {i + 1} ({pname}) qty_received is "
                    f"{ln.qty_received}, expected {qty} — agent did not "
                    f"validate the receipt at full demand"
                )

    # --- Picking: must exist, single, done, full qty -------------------
    pickings = po.picking_ids
    if len(pickings) == 0:
        failures.append(
            "No stock.picking found for the PO — unexpected (Confirm "
            "Order should auto-generate an incoming transfer)"
        )
    elif len(pickings) > 1:
        failures.append(
            f"Expected exactly 1 receipt, found {len(pickings)}: "
            f"{pickings.mapped('name')} — agent may have created a "
            f"backorder or split the receipt"
        )
    else:
        pick = pickings[0]
        if pick.state != "done":
            failures.append(
                f"Receipt state is '{pick.state}', expected 'done' — "
                f"agent did not click Validate (or Validate failed)"
            )
        if pick.backorder_id:
            failures.append(
                "Receipt has a backorder parent — unexpected; the full "
                "demand should have been received in one go"
            )

        # Move quantities
        for product_name, expected in (
            (PRODUCT_A, QTY_A),
            (PRODUCT_B, QTY_B),
        ):
            moves = pick.move_ids.filtered(
                lambda m, n=product_name: m.product_id.name == n
            )
            if len(moves) != 1:
                failures.append(
                    f"Receipt has {len(moves)} move(s) for "
                    f"'{product_name}', expected 1"
                )
            elif not _close(moves.quantity, expected):
                failures.append(
                    f"Receipt '{product_name}' Done qty is "
                    f"{moves.quantity}, expected {expected}"
                )

    # --- No vendor bill must exist for the vendor ----------------------
    bills = env["account.move"].search([
        ("move_type", "=", "in_invoice"),
        ("partner_id", "=", vendor.id),
    ])
    if bills:
        failures.append(
            f"Found {len(bills)} vendor bill(s) for '{VENDOR_NAME}' "
            f"(refs: {bills.mapped('ref')}); the task must NOT create a "
            f"bill — it stops at receipt validation (3-way match READY)"
        )

    return failures
