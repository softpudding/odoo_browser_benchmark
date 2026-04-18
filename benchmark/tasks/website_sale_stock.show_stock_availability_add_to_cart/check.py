"""Postcondition checks for website_sale_stock.show_stock_availability_add_to_cart.

Pass criteria:

  * ``Bench Limited Stock`` still exists, active, published, storable, with
    show_availability=True and available_threshold=100.
  * Some website sale.order (draft cart) contains exactly one line for
    ``Bench Limited Stock`` with product_uom_qty == 3.
  * The cart state is ``draft``.

We match the cart by line content (not by partner) because /shop is
``auth=public`` and the agent may not have logged in.
"""


PRODUCT_NAME = "Bench Limited Stock"
EXPECTED_QTY = 3.0


def check(env):
    failures = []

    tmpl = env["product.template"].with_context(active_test=False).search(
        [("name", "=", PRODUCT_NAME)], limit=1,
    )
    if not tmpl:
        return [f"Product {PRODUCT_NAME!r} is missing"]

    if not tmpl.active:
        failures.append(f"Product {PRODUCT_NAME!r} was archived")
    if not tmpl.is_published:
        failures.append(f"Product {PRODUCT_NAME!r} was unpublished")
    if not tmpl.is_storable:
        failures.append(f"Product {PRODUCT_NAME!r} is no longer storable")
    if not tmpl.show_availability:
        failures.append(
            f"Product show_availability flipped to False (expected True)"
        )
    if abs(tmpl.available_threshold - 100.0) > 0.001:
        failures.append(
            f"available_threshold is {tmpl.available_threshold}, expected 100"
        )

    # Find any website cart with a line for the seeded product.
    carts = env["sale.order"].search([
        ("website_id", "!=", False),
        ("order_line.product_template_id", "=", tmpl.id),
    ])
    if not carts:
        failures.append(f"No website cart contains a {PRODUCT_NAME!r} line")
        return failures

    cart = carts.sorted("write_date", reverse=True)[0]

    if cart.state != "draft":
        failures.append(f"Cart state is {cart.state!r}, expected 'draft'")

    target_lines = cart.order_line.filtered(
        lambda line: line.product_template_id.id == tmpl.id
    )
    if len(target_lines) != 1:
        failures.append(
            f"Expected exactly 1 {PRODUCT_NAME!r} line, got {len(target_lines)}"
        )
    elif abs(target_lines.product_uom_qty - EXPECTED_QTY) > 0.001:
        failures.append(
            f"{PRODUCT_NAME!r} qty is {target_lines.product_uom_qty}, "
            f"expected {EXPECTED_QTY}"
        )

    # No other random lines expected.
    extra_lines = cart.order_line.filtered(
        lambda line: line.product_template_id.id != tmpl.id
    )
    extra_names = sorted({line.product_template_id.name for line in extra_lines})
    if extra_names:
        failures.append(
            f"Cart contains unexpected extra product lines: {extra_names}"
        )

    return failures
