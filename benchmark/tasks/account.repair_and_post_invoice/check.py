"""Postcondition checks for account.repair_and_post_invoice."""


def check(env):
    failures = []

    target = env["account.move"].search([
        ("move_type", "=", "out_invoice"),
        ("invoice_origin", "=", "APR-OPS"),
    ], limit=1)
    if not target:
        return ["Target invoice APR-OPS not found"]

    if target.state != "posted":
        failures.append(f"Target invoice state is {target.state}, expected posted")

    expected = {
        "Acoustic Panel": (2.0, 5.0),
        "Focus Lamp": (1.0, 15.0),
        "Desk Shelf": (3.0, 0.0),
    }
    product_lines = target.invoice_line_ids.filtered(lambda line: line.product_id)
    seen = {line.product_id.display_name: line for line in product_lines}
    for product_name, (qty, discount) in expected.items():
        line = seen.get(product_name)
        if not line:
            failures.append(f"Missing invoice line for {product_name}")
            continue
        if line.quantity != qty:
            failures.append(f"{product_name} quantity is {line.quantity}, expected {qty}")
        if line.discount != discount:
            failures.append(f"{product_name} discount is {line.discount}, expected {discount}")

    if target.ref != "APR-OPS-READY":
        failures.append(f"Customer Reference is {target.ref!r}, expected 'APR-OPS-READY'")

    return failures

