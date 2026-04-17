"""Postcondition checks for account.create_refund_modify_reissue.

Validates:
- Original invoice (HLE-MOD-01) is fully reversed
- A credit note exists and is posted
- A new replacement invoice exists and is posted
- New invoice has Technical Audit qty = 5, Site Inspection qty = 3
- New invoice date = 2026-06-10
- Distractor invoice (HLS-DIST-01) unchanged
"""

from datetime import date


def check(env):
    failures = []

    # --- Original invoice must exist and be reversed ---
    target = env["account.move"].search([("ref", "=", "HLE-MOD-01")], limit=1)
    if not target:
        return ["Original invoice HLE-MOD-01 not found"]

    if target.payment_state != "reversed":
        failures.append(
            f"HLE-MOD-01 payment_state is '{target.payment_state}', "
            f"expected 'reversed' (Reverse and Create Invoice reconciles automatically)"
        )

    if target.state != "posted":
        failures.append(
            f"HLE-MOD-01 state is '{target.state}', expected 'posted'"
        )

    # --- Credit note must exist ---
    credit_notes = env["account.move"].search([
        ("reversed_entry_id", "=", target.id),
        ("move_type", "=", "out_refund"),
    ])
    if not credit_notes:
        failures.append("No credit note found linked to HLE-MOD-01")
    else:
        cn = credit_notes[0]
        if cn.state != "posted":
            failures.append(
                f"Credit note state is '{cn.state}', expected 'posted'"
            )
        # Credit note date should be 2026-06-05
        expected_cn_date = date(2026, 4, 10)
        if cn.date != expected_cn_date:
            failures.append(
                f"Credit note date is '{cn.date}', expected '{expected_cn_date}'"
            )

    # --- New replacement invoice must exist ---
    # The modify workflow creates a new draft invoice for the same partner.
    # It will not have ref=HLE-MOD-01 (that's the original). Find it by
    # looking for a posted out_invoice for Harborlight Engineering that is
    # NOT the original.
    partner = target.partner_id
    new_invoices = env["account.move"].search([
        ("partner_id", "=", partner.id),
        ("move_type", "=", "out_invoice"),
        ("id", "!=", target.id),
        ("state", "=", "posted"),
    ])

    if not new_invoices:
        failures.append(
            "No new posted invoice found for Harborlight Engineering "
            "(the modify workflow should create a replacement draft that gets confirmed)"
        )
        return failures

    # Take the most recently created one
    new_inv = new_invoices.sorted("id", reverse=True)[0]

    # Check invoice date = 2026-06-10
    expected_inv_date = date(2026, 6, 10)
    actual_date = new_inv.invoice_date or new_inv.date
    if actual_date != expected_inv_date:
        failures.append(
            f"New invoice date is '{actual_date}', expected '{expected_inv_date}'"
        )

    # Check line quantities
    product_lines = new_inv.invoice_line_ids.filtered(
        lambda l: l.display_type == "product"
    )

    if len(product_lines) != 2:
        failures.append(
            f"Expected 2 product lines on new invoice, found {len(product_lines)}"
        )
    else:
        audit_line = product_lines.filtered(
            lambda l: "Technical Audit" in (l.name or "") or
                      (l.product_id and "Technical Audit" in l.product_id.name)
        )
        inspection_line = product_lines.filtered(
            lambda l: "Site Inspection" in (l.name or "") or
                      (l.product_id and "Site Inspection" in l.product_id.name)
        )

        if not audit_line:
            failures.append("Technical Audit line not found on new invoice")
        elif abs(audit_line[0].quantity - 5.0) > 0.01:
            failures.append(
                f"Technical Audit qty is {audit_line[0].quantity}, expected 5.0"
            )

        if not inspection_line:
            failures.append("Site Inspection line not found on new invoice")
        elif abs(inspection_line[0].quantity - 3.0) > 0.01:
            failures.append(
                f"Site Inspection qty is {inspection_line[0].quantity}, expected 3.0"
            )

        # Verify prices were NOT changed
        if audit_line and abs(audit_line[0].price_unit - 200.0) > 0.01:
            failures.append(
                f"Technical Audit price_unit is {audit_line[0].price_unit}, "
                f"expected 200.0 (price should not be changed)"
            )
        if inspection_line and abs(inspection_line[0].price_unit - 150.0) > 0.01:
            failures.append(
                f"Site Inspection price_unit is {inspection_line[0].price_unit}, "
                f"expected 150.0 (price should not be changed)"
            )

    # --- Distractor invoice must be untouched ---
    distractor = env["account.move"].search([("ref", "=", "HLS-DIST-01")], limit=1)
    if not distractor:
        failures.append("Distractor invoice HLS-DIST-01 not found (was it deleted?)")
    else:
        if distractor.state != "posted":
            failures.append(
                f"HLS-DIST-01 state changed to '{distractor.state}', "
                f"should still be 'posted'"
            )
        if distractor.payment_state in ("reversed", "paid", "partial"):
            failures.append(
                f"HLS-DIST-01 payment_state is '{distractor.payment_state}', "
                f"should be 'not_paid'"
            )
        distractor_cns = env["account.move"].search([
            ("reversed_entry_id", "=", distractor.id),
        ])
        if distractor_cns:
            failures.append(
                f"HLS-DIST-01 has {len(distractor_cns)} credit note(s) - "
                f"should have none"
            )

    return failures
