"""Postcondition checks for event.configure_three_ticket_tiers."""


EVENT_NAME = "Summer DevCon 2026"
EXPECTED_TIERS = {
    "Early Bird": {"price": 99.00, "seats_max": 80},
    "Regular": {"price": 149.00, "seats_max": 200},
    "VIP": {"price": 299.00, "seats_max": 40},
}


def check(env):
    failures = []

    event = env["event.event"].search([("name", "=", EVENT_NAME)], limit=1)
    if not event:
        return [f"Event '{EVENT_NAME}' not found"]

    tickets = event.event_ticket_ids
    if len(tickets) != 3:
        failures.append(
            f"Expected exactly 3 ticket tiers on {EVENT_NAME}, "
            f"found {len(tickets)}"
        )

    by_name = {t.name: t for t in tickets}
    for name, want in EXPECTED_TIERS.items():
        t = by_name.get(name)
        if not t:
            failures.append(f"Ticket tier '{name}' missing")
            continue
        if abs((t.price or 0.0) - want["price"]) > 1e-2:
            failures.append(
                f"Tier '{name}' price is {t.price}, expected {want['price']}"
            )
        if (t.seats_max or 0) != want["seats_max"]:
            failures.append(
                f"Tier '{name}' seats_max is {t.seats_max}, "
                f"expected {want['seats_max']}"
            )

    return failures
