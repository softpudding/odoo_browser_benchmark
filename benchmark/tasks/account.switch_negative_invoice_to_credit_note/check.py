"""Postcondition checks for account.switch_negative_invoice_to_credit_note."""


def check(env):
    failures = []

    move = env["account.move"].search([("invoice_origin", "=", "RET-204")], limit=1)
    if not move:
        return ["Target move RET-204 not found"]

    if move.move_type != "out_refund":
        failures.append(f"Move type is {move.move_type!r}, expected 'out_refund'")
    if move.state != "posted":
        failures.append(f"Move state is {move.state!r}, expected 'posted'")
    if move.ref != "RET-204-REFUND":
        failures.append(f"Customer Reference is {move.ref!r}, expected 'RET-204-REFUND'")
    if move.amount_total <= 0:
        failures.append(f"Credit note total is {move.amount_total}, expected a positive amount")

    product_lines = move.invoice_line_ids.filtered(lambda line: line.product_id)
    if len(product_lines) != 1:
        failures.append(f"Expected exactly 1 product line, found {len(product_lines)}")
    elif product_lines[0].product_id.display_name != "Return Fee":
        failures.append(
            f"Credit note line product is {product_lines[0].product_id.display_name!r}, expected 'Return Fee'"
        )

    return failures

