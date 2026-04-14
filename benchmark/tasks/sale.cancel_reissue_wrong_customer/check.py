"""Postcondition checks for sale.cancel_reissue_wrong_customer."""


def check(env):
    failures = []

    east = env["res.partner"].search([("name", "=", "Harbor Retail East")], limit=1)
    west = env["res.partner"].search([("name", "=", "Harbor Retail West")], limit=1)
    if not east or not west:
        return ["Missing Harbor Retail customers for wrong-customer recovery task"]

    old_order = env["sale.order"].search([
        ("partner_id", "=", east.id),
        ("client_order_ref", "=", "SALE-FIX-12"),
    ], limit=1)
    if not old_order:
        failures.append("Original Harbor Retail East order not found")
    elif old_order.state != "cancel":
        failures.append(
            f"Original order state is {old_order.state!r}, expected 'cancel'"
        )

    new_orders = env["sale.order"].search([
        ("partner_id", "=", west.id),
        ("client_order_ref", "=", "SALE-FIX-12-WEST"),
    ])
    if not new_orders:
        failures.append("Replacement Harbor Retail West order not found")
        return failures
    if len(new_orders) > 1:
        failures.append(f"Expected 1 replacement order, found {len(new_orders)}")

    new_order = new_orders[0]
    if new_order.state != "sale":
        failures.append(f"Replacement order state is {new_order.state!r}, expected 'sale'")

    expected_lines = {
        "Counter Display": {"product_uom_qty": 4.0, "price_unit": 210.0},
        "Shelf Signage Kit": {"product_uom_qty": 7.0, "price_unit": 48.0},
    }

    product_lines = new_order.order_line.filtered(
        lambda line: line.display_type not in ("line_section", "line_note", "line_subsection")
        and line.product_id
    )
    if len(product_lines) != 2:
        failures.append(
            f"Replacement order has {len(product_lines)} product lines, expected 2"
        )

    for line in product_lines:
        name = line.product_id.name
        if name not in expected_lines:
            failures.append(f"Unexpected replacement line: {name}")
            continue
        expected = expected_lines.pop(name)
        for field, value in expected.items():
            actual = getattr(line, field)
            if abs(actual - value) > 0.01:
                failures.append(
                    f"Replacement line {name}.{field}: expected {value}, got {actual}"
                )

    for missing in expected_lines:
        failures.append(f"Missing replacement line: {missing}")

    return failures
