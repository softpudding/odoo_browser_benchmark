"""Postcondition checks for account.partial_refund_service_credit_note."""

from datetime import date


def check(env):
    failures = []

    target = env["account.move"].search([("ref", "=", "CN-SERVICE-01")], limit=1)
    if not target:
        return ["Invoice CN-SERVICE-01 not found"]

    if target.state != "posted":
        failures.append(f"CN-SERVICE-01 state is {target.state!r}, expected 'posted'")
    if target.payment_state != "partial":
        failures.append(
            f"CN-SERVICE-01 payment_state is {target.payment_state!r}, expected 'partial'"
        )

    credit_notes = env["account.move"].search([
        ("reversed_entry_id", "=", target.id),
        ("move_type", "=", "out_refund"),
    ])
    if not credit_notes:
        failures.append("No credit note found linked to CN-SERVICE-01")
        return failures
    if len(credit_notes) > 1:
        failures.append(f"Expected 1 credit note, found {len(credit_notes)}")

    credit_note = credit_notes[0]
    if credit_note.state != "posted":
        failures.append(f"Credit note state is {credit_note.state!r}, expected 'posted'")
    if credit_note.date != date(2026, 5, 5):
        failures.append(
            f"Credit note date is {credit_note.date!r}, expected 2026-05-05"
        )
    if "Warehouse Audit session canceled" not in (credit_note.ref or ""):
        failures.append(
            f"Credit note ref is {credit_note.ref!r}, expected the reason text to be present"
        )

    product_lines = credit_note.invoice_line_ids.filtered(
        lambda line: line.display_type == "product"
    )
    if len(product_lines) != 1:
        failures.append(
            f"Expected 1 product line on the credit note, found {len(product_lines)}"
        )
    else:
        line = product_lines[0]
        if line.product_id.name != "Warehouse Audit":
            failures.append(
                f"Credit note product is {line.product_id.name!r}, expected 'Warehouse Audit'"
            )
        if abs(line.quantity - 1.0) > 0.01:
            failures.append(
                f"Credit note quantity is {line.quantity}, expected 1.0"
            )
        if abs(line.price_unit - 475.0) > 0.01:
            failures.append(
                f"Credit note price_unit is {line.price_unit}, expected 475.0"
            )

    if credit_note.invoice_line_ids.filtered(lambda line: line.product_id.name == "Onsite Training"):
        failures.append("Onsite Training should not appear on the credit note")

    distractor = env["account.move"].search([("ref", "=", "CN-SERVICE-02")], limit=1)
    if not distractor:
        failures.append("Invoice CN-SERVICE-02 not found (was it deleted?)")
    else:
        if distractor.state != "posted":
            failures.append(
                f"CN-SERVICE-02 state changed to {distractor.state!r}, expected 'posted'"
            )
        if env["account.move"].search_count([("reversed_entry_id", "=", distractor.id)]):
            failures.append("CN-SERVICE-02 should not have any credit notes")

    return failures
