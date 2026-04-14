"""Postcondition checks for account.switch_negative_invoice_repair_credit_note."""


def check(env):
    failures = []

    move = env["account.move"].search([("invoice_origin", "=", "RET-508")], limit=1)
    if not move:
        return ["Target move RET-508 not found"]

    if move.move_type != "out_refund":
        failures.append(f"Move type is {move.move_type!r}, expected 'out_refund'")
    if move.state != "posted":
        failures.append(f"Move state is {move.state!r}, expected 'posted'")
    if move.ref != "RET-508-READY":
        failures.append(f"Customer Reference is {move.ref!r}, expected 'RET-508-READY'")

    expected = {
        "Return Fee": (1.0, 0.0),
        "Service Retainer": (2.0, 10.0),
        "Restocking Surcharge": (1.0, 5.0),
    }
    product_lines = move.invoice_line_ids.filtered(lambda line: line.product_id)
    seen = {line.product_id.display_name: line for line in product_lines}
    for product_name, (qty, discount) in expected.items():
        line = seen.get(product_name)
        if not line:
            failures.append(f"Missing credit note line for {product_name}")
            continue
        if line.quantity != qty:
            failures.append(f"{product_name} quantity is {line.quantity}, expected {qty}")
        if line.discount != discount:
            failures.append(f"{product_name} discount is {line.discount}, expected {discount}")

    if move.amount_total <= 0:
        failures.append(f"Credit note total is {move.amount_total}, expected a positive amount")

    return failures
