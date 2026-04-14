"""Postcondition checks for account.create_credit_note_and_reconcile.

Validates: partial credit note created and posted for the correct invoice,
with correct reason, date, and partial quantity. Distractor untouched.
"""

from datetime import date


def check(env):
    failures = []

    # Target invoice must exist
    target = env["account.move"].search([("ref", "=", "CN-TARGET-01")], limit=1)
    if not target:
        return ["Invoice CN-TARGET-01 not found"]

    # Should have partial payment status (not fully reversed since qty is partial)
    if target.payment_state not in ("partial", "in_payment", "reversed"):
        failures.append(
            f"CN-TARGET-01 payment_state is '{target.payment_state}', "
            f"expected 'partial' or 'in_payment'"
        )

    # Find the credit note (reversal)
    credit_notes = env["account.move"].search([
        ("reversed_entry_id", "=", target.id),
        ("move_type", "=", "out_refund"),
    ])

    if not credit_notes:
        failures.append("No credit note found linked to CN-TARGET-01")
        return failures

    if len(credit_notes) > 1:
        failures.append(f"Expected 1 credit note, found {len(credit_notes)}")

    cn = credit_notes[0]

    # Credit note must be posted
    if cn.state != "posted":
        failures.append(f"Credit note state is '{cn.state}', expected 'posted'")

    # Credit note date must be 2026-04-30
    expected_date = date(2026, 4, 30)
    if cn.date != expected_date:
        failures.append(
            f"Credit note date is '{cn.date}', expected '{expected_date}'"
        )

    # Check partial quantity: should be 10, not 18
    product_lines = cn.invoice_line_ids.filtered(
        lambda l: l.display_type == "product"
    )
    if len(product_lines) != 1:
        failures.append(f"Expected 1 product line on credit note, found {len(product_lines)}")
    else:
        line = product_lines[0]
        if abs(line.quantity - 10.0) > 0.01:
            failures.append(
                f"Credit note qty is {line.quantity}, expected 10.0 (partial credit)"
            )

    # Check reason in narration
    if cn.narration and "Partial delivery" not in (cn.narration or ""):
        failures.append(
            f"Credit note reason should contain 'Partial delivery'"
        )

    # Distractor invoice must NOT be reversed or modified
    distractor = env["account.move"].search([("ref", "=", "CN-IGNORE-01")], limit=1)
    if not distractor:
        failures.append("Invoice CN-IGNORE-01 not found (was it deleted?)")
    else:
        if distractor.payment_state in ("reversed", "in_payment", "paid", "partial"):
            failures.append(
                f"CN-IGNORE-01 should NOT be reversed/paid, but payment_state is "
                f"'{distractor.payment_state}'"
            )
        if distractor.state != "posted":
            failures.append(
                f"CN-IGNORE-01 state changed to '{distractor.state}', "
                f"should still be 'posted'"
            )
        distractor_cns = env["account.move"].search([
            ("reversed_entry_id", "=", distractor.id),
        ])
        if distractor_cns:
            failures.append(
                f"CN-IGNORE-01 has {len(distractor_cns)} credit note(s) — "
                f"should have none"
            )

    return failures
