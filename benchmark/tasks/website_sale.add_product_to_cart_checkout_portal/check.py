"""Postcondition checks for website_sale.add_product_to_cart_checkout_portal."""


PRODUCT_NAME = "Bench Portal Product"
CUSTOMER_NAME = "Bench Portal Customer"
EXPECTED_TOTAL = 25.0


def check(env):
    failures = []

    partners = env["res.partner"].with_context(active_test=False).search(
        [("name", "=", CUSTOMER_NAME)]
    )
    if not partners:
        return [f"res.partner '{CUSTOMER_NAME}' not found (address never saved)"]
    if len(partners) > 1:
        failures.append(
            f"Expected exactly 1 partner named '{CUSTOMER_NAME}',"
            f" found {len(partners)}"
        )

    orders = env["sale.order"].with_context(active_test=False).search([
        ("partner_id", "in", partners.ids),
    ])
    if not orders:
        return failures + [
            f"No sale.order for customer '{CUSTOMER_NAME}' found"
            " (checkout never produced a backend order)"
        ]
    if len(orders) > 1:
        failures.append(
            f"Expected exactly 1 sale.order for '{CUSTOMER_NAME}',"
            f" found {len(orders)}"
        )

    order = orders[0]

    if order.state not in ("sale", "sent", "done"):
        failures.append(
            f"Order state is '{order.state}', expected one of"
            " ('sale','sent','done') — the order must be confirmed"
            " (not left as a draft quotation or cancelled)"
        )

    if not order.website_id:
        failures.append(
            "Order has no website_id set; the order must be placed through"
            " the public web shop, not created directly in the backend"
        )

    product_lines = order.order_line
    if len(product_lines) < 1:
        failures.append("Order has no order lines")
    else:
        # Ignore reward/zero-price auxiliary lines that some modules add,
        # just verify at least one line for the seeded product with qty 1
        # and price 25.00.
        match = product_lines.filtered(
            lambda l: l.product_id.product_tmpl_id.name == PRODUCT_NAME
        )
        if len(match) != 1:
            failures.append(
                f"Expected exactly 1 order line for '{PRODUCT_NAME}',"
                f" found {len(match)}"
            )
        else:
            pline = match[0]
            if abs(pline.product_uom_qty - 1.0) > 0.01:
                failures.append(
                    f"Product line qty is {pline.product_uom_qty}, expected 1.0"
                )
            if abs(pline.price_unit - 25.0) > 0.05:
                failures.append(
                    f"Product line price_unit is {pline.price_unit}, expected 25.00"
                )

    if abs(order.amount_total - EXPECTED_TOTAL) > 0.05:
        failures.append(
            f"Order amount_total is {order.amount_total},"
            f" expected {EXPECTED_TOTAL}"
        )

    # Address sanity — at minimum a street and country should be on the
    # order's partner_id so we know the delivery address step was completed.
    order_partner = order.partner_id
    if not order_partner.street:
        failures.append(
            "Order partner has no street set; address form was not filled"
        )
    if not order_partner.country_id:
        failures.append(
            "Order partner has no country set; address form was not filled"
        )

    return failures
