"""Postcondition checks for account.credit_note_partial_refund_post."""


def check(env):
    failures = []

    target = env["account.move"].search([("ref", "=", "INV/BENCH/001")], limit=1)
    if not target:
        return ["Source invoice INV/BENCH/001 not found"]

    if target.move_type != "out_invoice":
        failures.append(
            f"INV/BENCH/001 move_type is {target.move_type!r}, expected 'out_invoice'"
        )
    if target.state != "posted":
        failures.append(
            f"INV/BENCH/001 state is {target.state!r}, expected 'posted' "
            f"(source invoice must not be reset to draft or cancelled)"
        )

    credit_notes = env["account.move"].search([
        ("reversed_entry_id", "=", target.id),
        ("move_type", "=", "out_refund"),
    ])
    if not credit_notes:
        failures.append(
            "No out_refund credit note with reversed_entry_id=INV/BENCH/001 found"
        )
        return failures
    if len(credit_notes) > 1:
        failures.append(
            f"Expected exactly 1 linked credit note, found {len(credit_notes)}"
        )

    cn = credit_notes[0]
    if cn.state != "posted":
        failures.append(
            f"Credit note state is {cn.state!r}, expected 'posted'"
        )
    if cn.partner_id.id != target.partner_id.id:
        failures.append(
            f"Credit note partner is {cn.partner_id.name!r}, "
            f"expected {target.partner_id.name!r}"
        )

    # Reason text should be carried into the credit note ref
    if "Wrong qty" not in (cn.ref or ""):
        failures.append(
            f"Credit note ref is {cn.ref!r}, expected to contain 'Wrong qty'"
        )

    product_lines = cn.invoice_line_ids.filtered(
        lambda line: line.display_type == "product"
    )
    if len(product_lines) != 1:
        failures.append(
            f"Expected 1 product line on credit note, found {len(product_lines)}"
        )
    else:
        line = product_lines[0]
        if line.product_id.name != "Bench Item A":
            failures.append(
                f"Credit note product is {line.product_id.name!r}, "
                f"expected 'Bench Item A'"
            )
        if abs(line.quantity - 2.0) > 0.01:
            failures.append(
                f"Credit note Item A quantity is {line.quantity}, expected 2.0"
            )
        if abs(line.price_unit - 100.0) > 0.01:
            failures.append(
                f"Credit note Item A price_unit is {line.price_unit}, expected 100.0"
            )

    if cn.invoice_line_ids.filtered(
        lambda l: l.product_id.name == "Bench Item B"
    ):
        failures.append(
            "Bench Item B should NOT appear on the credit note (agent must delete it)"
        )

    if abs(cn.amount_total - 200.0) > 0.01:
        failures.append(
            f"Credit note amount_total is {cn.amount_total}, expected 200.0"
        )
    if abs(cn.amount_untaxed - 200.0) > 0.01:
        failures.append(
            f"Credit note amount_untaxed is {cn.amount_untaxed}, expected 200.0"
        )

    # Source invoice totals and lines must be unchanged
    if abs(target.amount_total - 500.0) > 0.01:
        failures.append(
            f"Source invoice amount_total changed to {target.amount_total}, "
            f"expected 500.0 (invoice must be untouched)"
        )
    target_product_lines = target.invoice_line_ids.filtered(
        lambda line: line.display_type == "product"
    )
    if len(target_product_lines) != 2:
        failures.append(
            f"Source invoice now has {len(target_product_lines)} product lines, "
            f"expected 2"
        )

    return failures
