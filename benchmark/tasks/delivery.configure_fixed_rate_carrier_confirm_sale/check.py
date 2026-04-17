"""Postcondition checks for delivery.configure_fixed_rate_carrier_confirm_sale."""


def check(env):
    failures = []

    carrier = env["delivery.carrier"].search([("name", "=", "Harbor Flat Freight")], limit=1)
    if not carrier:
        return ["Delivery method 'Harbor Flat Freight' not found"]

    if carrier.delivery_type != "fixed":
        failures.append(f"Delivery type is '{carrier.delivery_type}', expected 'fixed'")
    if abs(carrier.fixed_price - 18.5) > 0.0001:
        failures.append(f"Fixed price is {carrier.fixed_price}, expected 18.5")

    order = env["sale.order"].search([("client_order_ref", "=", "HARBOR-SHIP-01")], limit=1)
    if not order:
        failures.append("Target quotation with customer reference HARBOR-SHIP-01 not found")
        return failures

    if order.state != "sale":
        failures.append(f"Order state is '{order.state}', expected 'sale'")
    if order.carrier_id.id != carrier.id:
        failures.append(
            f"Order delivery method is '{order.carrier_id.name or 'unset'}', expected 'Harbor Flat Freight'"
        )

    delivery_lines = order.order_line.filtered("is_delivery")
    if len(delivery_lines) != 1:
        failures.append(f"Expected exactly 1 delivery line, found {len(delivery_lines)}")
    else:
        if abs(delivery_lines[0].price_unit - 18.5) > 0.0001:
            failures.append(
                f"Delivery line price is {delivery_lines[0].price_unit}, expected 18.5"
            )

    return failures
