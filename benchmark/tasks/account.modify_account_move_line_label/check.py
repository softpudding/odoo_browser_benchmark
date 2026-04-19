"""Postcondition checks for account.modify_account_move_line_label.

Validates:
  1. Invoice BENCH-EDIT-001 ends in state='posted' (out_invoice).
  2. The invoice has exactly one product (non-section, non-tax) line
     whose `name` effectively contains 'Corrected description'.
  3. amount_total is unchanged at 100.00.
  4. The agent did not change the partner.

Note on the stored label format:
Odoo 19's `product_label_section_and_note_field` widget concatenates
`productName + "\\n" + label` when both are set. So when a human or
agent types "Corrected description" into the Label cell on a line with
a linked product, the stored `name` becomes either:
  - "Corrected description" (if the product was cleared first), or
  - "Bench Edit Service\\nCorrected description" (product+label concat).
Both outcomes mean the user-visible Label is "Corrected description"
(the widget's `label` getter strips productName from the stored text
when rendering). We accept either form.
"""

PRODUCT_NAME = "Bench Edit Service"
TARGET_REF = "BENCH-EDIT-001"
PARTNER_NAME = "Bench Edit Co"
EXPECTED_LABEL = "Corrected description"
EXPECTED_AMOUNT = 100.0


def _label_matches(stored: str, expected: str, product_name: str) -> bool:
    """Return True if the stored name resolves to the expected label.

    Accepts either exact match or `<product_name>\\n<expected>` concat.
    """
    if not stored:
        return False
    s = stored.strip()
    if s == expected:
        return True
    # Strip product_name prefix (if widget concatenated) then compare.
    if product_name and product_name in s:
        stripped = s.replace(product_name, "").strip()
        if stripped == expected:
            return True
    return False


def check(env):
    failures = []

    inv = env["account.move"].search(
        [("ref", "=", TARGET_REF)], limit=1
    )
    if not inv:
        return [f"Target invoice {TARGET_REF!r} not found"]

    if inv.move_type != "out_invoice":
        failures.append(
            f"Invoice move_type is {inv.move_type!r}, expected 'out_invoice'"
        )

    if inv.state != "posted":
        failures.append(
            f"Invoice state is {inv.state!r}, expected 'posted' "
            f"(did you click Confirm after editing the label?)"
        )

    if inv.partner_id.name != PARTNER_NAME:
        failures.append(
            f"Invoice partner is {inv.partner_id.name!r}, "
            f"expected {PARTNER_NAME!r}"
        )

    # Amount sanity: agent must not edit the price/quantity.
    if abs(inv.amount_total - EXPECTED_AMOUNT) > 0.01:
        failures.append(
            f"Invoice amount_total is {inv.amount_total}, "
            f"expected {EXPECTED_AMOUNT} — the agent should only change "
            f"the Label, not Quantity or Unit Price."
        )

    # Inspect invoice lines: exactly one product line with the corrected label.
    product_lines = inv.invoice_line_ids.filtered(
        lambda l: l.display_type not in (
            "line_section", "line_subsection", "line_note"
        )
    )
    if len(product_lines) != 1:
        failures.append(
            f"Expected exactly 1 product line, found {len(product_lines)} "
            f"(labels: {product_lines.mapped('name')!r})"
        )
        return failures

    line = product_lines[0]
    if not _label_matches(line.name or "", EXPECTED_LABEL, PRODUCT_NAME):
        failures.append(
            f"Invoice line label (name) is {line.name!r}, expected "
            f"{EXPECTED_LABEL!r} (either as-is or concatenated with the "
            f"product name via the product_label_section_and_note_field "
            f"widget, i.e. {PRODUCT_NAME!r} + newline + {EXPECTED_LABEL!r})"
        )

    if abs(line.price_unit - 100.0) > 0.01:
        failures.append(
            f"Invoice line price_unit is {line.price_unit}, expected 100.0 "
            f"(only the Label should change)"
        )
    if abs(line.quantity - 1.0) > 0.01:
        failures.append(
            f"Invoice line quantity is {line.quantity}, expected 1.0 "
            f"(only the Label should change)"
        )

    return failures
