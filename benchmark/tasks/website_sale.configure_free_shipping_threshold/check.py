"""Postcondition checks for website_sale.configure_free_shipping_threshold."""


CARRIER_NAME = "Bench Ship"


def check(env):
    failures = []

    carriers = env["delivery.carrier"].with_context(active_test=False).search(
        [("name", "=", CARRIER_NAME)]
    )
    if not carriers:
        return [f"delivery.carrier '{CARRIER_NAME}' not found"]
    if len(carriers) > 1:
        failures.append(
            f"Expected exactly 1 delivery.carrier named '{CARRIER_NAME}',"
            f" found {len(carriers)}"
        )
    carrier = carriers[0]

    if not carrier.active:
        failures.append(f"Carrier '{CARRIER_NAME}' is archived; must be active")

    if carrier.delivery_type != "fixed":
        failures.append(
            f"Carrier delivery_type is '{carrier.delivery_type}',"
            f" expected 'fixed' (do not change the provider)"
        )

    if abs(carrier.fixed_price - 15.0) > 0.01:
        failures.append(
            f"Carrier fixed_price is {carrier.fixed_price},"
            f" expected 15.0 (do not edit the shipping price)"
        )

    if not carrier.free_over:
        failures.append(
            "Carrier free_over is False; the 'Free if order amount is above'"
            " checkbox must be enabled"
        )

    if abs(carrier.amount - 100.0) > 0.01:
        failures.append(
            f"Carrier amount is {carrier.amount}, expected 100.00"
            " (the free-shipping threshold must be exactly 100)"
        )

    return failures
