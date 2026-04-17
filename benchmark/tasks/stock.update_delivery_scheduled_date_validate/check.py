"""Postcondition checks for stock.update_delivery_scheduled_date_validate."""

from datetime import date, datetime, timedelta


def check(env):
    failures = []
    target = env["stock.picking"].search([("origin", "=", "BENCH-DEL-DATE-01")], limit=1)
    if not target:
        return ["Target delivery 'BENCH-DEL-DATE-01' not found"]
    if target.state != "done":
        failures.append(f"Target delivery state is '{target.state}', expected 'done'")
    actual_date = target.scheduled_date
    if isinstance(actual_date, datetime):
        actual_date = (actual_date + timedelta(hours=8)).date()
    if actual_date != date(2026, 5, 27):
        failures.append(f"Scheduled date is {actual_date}, expected 2026-05-27")
    for name, expected in [('Steel Bracket 12"', 20), ('Copper Wire 100m', 8)]:
        move = target.move_ids.filtered(lambda m: m.product_id.name == name)
        if not move:
            failures.append(f"Missing move for {name}")
            continue
        delivered = getattr(move, 'quantity', None)
        if delivered is None:
            delivered = move.quantity_done
        if abs(delivered - expected) > 0.001:
            failures.append(f"{name} delivered qty is {delivered}, expected {expected}")
    distractor = env["stock.picking"].search([("origin", "=", "BENCH-DEL-DATE-OTHER")], limit=1)
    if distractor and distractor.state == 'done':
        failures.append("Distractor delivery was validated")
    return failures
