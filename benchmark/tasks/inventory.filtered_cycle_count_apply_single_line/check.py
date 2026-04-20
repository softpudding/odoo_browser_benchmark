"""Check inventory.filtered_cycle_count_apply_single_line."""


def check(env):
    failures = []
    quants = env["stock.quant"].search([
        ("product_id.name", "=", "Bench Cycle Rotor"),
        ("location_id.complete_name", "in", ["WH/Cycle Bin", "WH/Stock"]),
    ])
    target = quants.filtered(lambda q: q.location_id.complete_name == "WH/Cycle Bin")[:1]
    other = quants.filtered(lambda q: q.location_id.complete_name == "WH/Stock")[:1]
    if not target:
        return ["Target quant at WH/Cycle Bin not found"]
    if abs(target.quantity - 11.0) > 0.0001:
        failures.append(f"Target quantity is {target.quantity}, expected 11.0")
    if not other:
        failures.append("Distractor quant at WH/Stock not found")
    elif abs(other.quantity - 4.0) > 0.0001:
        failures.append(f"Distractor quantity is {other.quantity}, expected 4.0")
    return failures
