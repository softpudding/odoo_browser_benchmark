"""Postcondition checks for sale.add_line_with_optional_template_apply_discount.

Validates:
1. Quotation S-BENCH-OPT-001 exists and is still draft.
2. The original Bench Hardware Kit line is unchanged (qty 3, discount 0).
3. A new Bench Service Bundle line exists with qty 2 and discount 10.
4. No extra lines were created or deleted.
"""

ORDER_REF = "S-BENCH-OPT-001"
EXISTING_PRODUCT = "Bench Hardware Kit"
NEW_PRODUCT = "Bench Service Bundle"


def check(env):
    failures = []

    order = env["sale.order"].search([
        ("client_order_ref", "=", ORDER_REF),
    ], limit=1)

    if not order:
        return [f"Quotation with reference '{ORDER_REF}' not found"]

    if order.state != "draft":
        failures.append(f"Quotation state is '{order.state}', expected 'draft'")

    hw_lines = order.order_line.filtered(
        lambda l: l.product_id.name == EXISTING_PRODUCT
    )
    if len(hw_lines) != 1:
        failures.append(
            f"Expected exactly 1 '{EXISTING_PRODUCT}' line, found {len(hw_lines)}"
        )
    else:
        hw = hw_lines[0]
        if hw.product_uom_qty != 3:
            failures.append(
                f"'{EXISTING_PRODUCT}' qty changed to {hw.product_uom_qty}, expected 3"
            )
        if hw.discount != 0.0:
            failures.append(
                f"'{EXISTING_PRODUCT}' discount changed to {hw.discount}%, expected 0%"
            )

    sb_lines = order.order_line.filtered(
        lambda l: l.product_id.name == NEW_PRODUCT
    )
    if len(sb_lines) != 1:
        failures.append(
            f"Expected exactly 1 '{NEW_PRODUCT}' line, found {len(sb_lines)}"
        )
    else:
        sb = sb_lines[0]
        if sb.product_uom_qty != 2:
            failures.append(
                f"'{NEW_PRODUCT}' qty is {sb.product_uom_qty}, expected 2"
            )
        if sb.discount != 10.0:
            failures.append(
                f"'{NEW_PRODUCT}' discount is {sb.discount}%, expected 10%"
            )

    # Total non-section/non-note lines should be exactly 2.
    real_lines = order.order_line.filtered(
        lambda l: not l.display_type
    )
    if len(real_lines) != 2:
        failures.append(
            f"Expected exactly 2 product lines, found {len(real_lines)}"
        )

    return failures
