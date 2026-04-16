"""Postcondition checks for account.create_bill_from_confirmed_po.

Validates:
1. A posted vendor bill exists with ref 'MSC-BILL-9921' for vendor
   Meridian Supply Co.
2. Bill Date (invoice_date) is 2026-05-03.
3. The bill is linked to the source PO (via invoice_origin or related
   purchase order).
4. Source PO state is still 'purchase' (not cancelled).
"""

from datetime import date


def check(env):
    failures = []

    vendor = env["res.partner"].search(
        [("name", "=", "Meridian Supply Co")], limit=1
    )
    if not vendor:
        return ["Vendor 'Meridian Supply Co' not found"]

    po = env["purchase.order"].search(
        [("partner_ref", "=", "BENCH-BILL-PO")], limit=1
    )
    if not po:
        failures.append("Source PO 'BENCH-BILL-PO' not found")
    elif po.state != "purchase":
        failures.append(
            f"Source PO state is '{po.state}', expected 'purchase'"
        )

    bill = env["account.move"].search([
        ("ref", "=", "MSC-BILL-9921"),
        ("move_type", "=", "in_invoice"),
    ], limit=1)
    if not bill:
        return failures + ["Vendor bill with ref 'MSC-BILL-9921' not found"]

    if bill.partner_id.id != vendor.id:
        failures.append(
            f"Bill vendor is '{bill.partner_id.display_name}', "
            "expected 'Meridian Supply Co'"
        )
    if bill.state != "posted":
        failures.append(
            f"Bill state is '{bill.state}', expected 'posted'"
        )
    if bill.invoice_date != date(2026, 5, 3):
        failures.append(
            f"Bill Date is {bill.invoice_date}, expected 2026-05-03"
        )

    # Linkage check: invoice_origin should contain the PO name, or
    # the bill's line partner_id should match.
    if po and po.name and po.name not in (bill.invoice_origin or ""):
        # Odoo 19 links via invoice_line_ids.purchase_line_id
        linked = bill.invoice_line_ids.mapped("purchase_line_id.order_id")
        if po not in linked:
            failures.append(
                f"Bill is not linked to PO '{po.name}' "
                f"(invoice_origin='{bill.invoice_origin}')"
            )

    return failures
