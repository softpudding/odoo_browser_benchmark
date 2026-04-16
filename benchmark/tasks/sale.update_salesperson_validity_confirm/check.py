"""Postcondition checks for sale.update_salesperson_validity_confirm."""


def check(env):
    failures = []

    order = env["sale.order"].search([("name", "=", "S-QUOTE-VAL-01")], limit=1)
    if not order:
        return ["Quotation 'S-QUOTE-VAL-01' not found"]

    if order.state != "sale":
        failures.append(f"Quotation state is '{order.state}', expected 'sale'")
    if order.user_id.name != "Marc Demo":
        failures.append(f"Salesperson is '{order.user_id.name}', expected 'Marc Demo'")
    if str(order.validity_date) != "2026-06-25":
        failures.append(
            f"Validity date is {order.validity_date}, expected 2026-06-25"
        )
    if order.client_order_ref != "CGS-JUNE":
        failures.append(
            f"Customer reference is '{order.client_order_ref}', expected 'CGS-JUNE'"
        )

    expected_lines = {
        "Studio Lighting Kit": (3.0, 320.0),
        "Backdrop Stand": (2.0, 180.0),
    }
    seen = {}
    for line in order.order_line.filtered(lambda l: not l.display_type):
        seen[line.product_id.name] = (float(line.product_uom_qty), float(line.price_unit))
    for product_name, expected in expected_lines.items():
        if seen.get(product_name) != expected:
            failures.append(
                f"Line '{product_name}' is {seen.get(product_name)}, expected {expected}"
            )

    distractor = env["sale.order"].search([("name", "=", "S-QUOTE-VAL-02")], limit=1)
    if not distractor:
        failures.append("Distractor quotation 'S-QUOTE-VAL-02' not found")
    else:
        if distractor.state != "draft":
            failures.append(
                f"Distractor quotation state is '{distractor.state}', expected 'draft'"
            )
        if distractor.client_order_ref:
            failures.append("Distractor quotation should not have a customer reference")

    return failures
