"""Postcondition checks for account.refund_customer_invoice_cash_basis."""


def check(env):
    failures = []

    target = env["account.move"].search(
        [("ref", "=", "BENCH-REFUND-001")], limit=1
    )
    if not target:
        return ["Source invoice BENCH-REFUND-001 not found"]

    if target.move_type != "out_invoice":
        failures.append(
            f"BENCH-REFUND-001 move_type is {target.move_type!r}, expected 'out_invoice'"
        )
    if target.state != "posted":
        failures.append(
            f"BENCH-REFUND-001 state is {target.state!r}, expected 'posted' "
            f"(source invoice must not be reset to draft or cancelled)"
        )

    # Source invoice totals/lines must be untouched.
    if abs(target.amount_total - 500.0) > 0.01:
        failures.append(
            f"Source invoice amount_total changed to {target.amount_total}, "
            f"expected 500.0 (invoice must be untouched)"
        )
    target_product_lines = target.invoice_line_ids.filtered(
        lambda line: line.display_type == "product"
    )
    if len(target_product_lines) != 1:
        failures.append(
            f"Source invoice now has {len(target_product_lines)} product lines, "
            f"expected 1 (invoice must be untouched)"
        )

    credit_notes = env["account.move"].search([
        ("reversed_entry_id", "=", target.id),
        ("move_type", "=", "out_refund"),
    ])
    if not credit_notes:
        failures.append(
            "No out_refund credit note with reversed_entry_id=BENCH-REFUND-001 found"
        )
        return failures
    if len(credit_notes) > 1:
        failures.append(
            f"Expected exactly 1 linked credit note, found {len(credit_notes)}"
        )

    cn = credit_notes[0]
    if cn.state != "posted":
        failures.append(
            f"Credit note state is {cn.state!r}, expected 'posted' "
            f"(must click header Confirm to post the draft credit note)"
        )
    if cn.partner_id.id != target.partner_id.id:
        failures.append(
            f"Credit note partner is {cn.partner_id.name!r}, "
            f"expected {target.partner_id.name!r}"
        )

    # Ref must reference the source and include the reason.
    if "Reversal of:" not in (cn.ref or ""):
        failures.append(
            f"Credit note ref is {cn.ref!r}, expected to contain 'Reversal of:'"
        )
    if target.name and target.name not in (cn.ref or ""):
        failures.append(
            f"Credit note ref is {cn.ref!r}, expected to contain the source "
            f"name {target.name!r}"
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
        if line.product_id.name != "Bench Refund Service":
            failures.append(
                f"Credit note product is {line.product_id.name!r}, "
                f"expected 'Bench Refund Service'"
            )
        if abs(line.quantity - 1.0) > 0.01:
            failures.append(
                f"Credit note quantity is {line.quantity}, expected 1.0 "
                f"(keep qty at 1, reduce price_unit instead)"
            )
        if abs(line.price_unit - 200.0) > 0.01:
            failures.append(
                f"Credit note price_unit is {line.price_unit}, expected 200.0 "
                f"(agent must override the default 500.0 price_unit)"
            )

    if abs(cn.amount_total - 200.0) > 0.01:
        failures.append(
            f"Credit note amount_total is {cn.amount_total}, expected 200.0 "
            f"(full-refund 500.0 indicates the agent accepted the wizard "
            f"default without editing price_unit)"
        )
    if abs(cn.amount_untaxed - 200.0) > 0.01:
        failures.append(
            f"Credit note amount_untaxed is {cn.amount_untaxed}, expected 200.0"
        )

    return failures
