"""Postcondition checks for delivery.country_rule_and_free_threshold_apply_to_so."""


def check(env):
    failures = []

    carrier = env["delivery.carrier"].search([
        ("name", "=", "US Harbor Freight"),
    ], limit=1)
    if not carrier:
        return ["Delivery method 'US Harbor Freight' not found"]

    us = env["res.country"].search([("code", "=", "US")], limit=1)
    ca = env["res.country"].search([("code", "=", "CA")], limit=1)

    if carrier.delivery_type != "fixed":
        failures.append(
            f"Delivery type is {carrier.delivery_type!r}, expected 'fixed'"
        )
    if abs((carrier.fixed_price or 0.0) - 15.0) > 1e-4:
        failures.append(
            f"Fixed price is {carrier.fixed_price}, expected 15.0"
        )
    if not carrier.free_over:
        failures.append("Free-over threshold is not enabled")
    if abs((carrier.amount or 0.0) - 100.0) > 1e-4:
        failures.append(
            f"Free-over amount is {carrier.amount}, expected 100.0"
        )
    if carrier.country_ids != us:
        failures.append(
            f"Carrier countries are {carrier.country_ids.mapped('code')}, expected ['US']"
        )
    if ca in carrier.country_ids:
        failures.append("Carrier should not be available for Canada")

    target = env["sale.order"].search([
        ("client_order_ref", "=", "SHIP-US-100"),
    ], limit=1)
    distractor = env["sale.order"].search([
        ("client_order_ref", "=", "SHIP-CA-100"),
    ], limit=1)
    if not target or not distractor:
        failures.append("Target or distractor quotation is missing")
        return failures

    if target.state != "sale":
        failures.append(f"Target order state is {target.state!r}, expected 'sale'")
    if target.carrier_id != carrier:
        failures.append(
            f"Target order carrier is {target.carrier_id.name or 'unset'!r}, expected 'US Harbor Freight'"
        )

    delivery_lines = target.order_line.filtered("is_delivery")
    if len(delivery_lines) != 1:
        failures.append(
            f"Expected exactly 1 delivery line on target order, found {len(delivery_lines)}"
        )
    else:
        if abs(delivery_lines[0].price_unit or 0.0) > 1e-4:
            failures.append(
                f"Delivery line price is {delivery_lines[0].price_unit}, expected 0.0 from free-over threshold"
            )

    if distractor.state != "draft":
        failures.append(
            f"Distractor order state is {distractor.state!r}, expected 'draft'"
        )
    if distractor.carrier_id:
        failures.append("Distractor order should not have a carrier assigned")
    if distractor.order_line.filtered("is_delivery"):
        failures.append("Distractor order should not have a delivery line")

    return failures
