"""Postcondition checks for mrp.create_routing_set_workcenter.

Validates:
1. Work Center 'Benchmark Assembly Station' exists and is active.
2. BOM for product 'Benchmark Frame Assembly' has exactly one operation.
3. That operation is named 'Final Assembly', references the new work center,
   and has time_cycle_manual approximately 30 minutes.
4. The existing 2 BOM components were NOT modified/deleted.
"""


WORKCENTER_NAME = "Benchmark Assembly Station"
PRODUCT_NAME = "Benchmark Frame Assembly"


def check(env):
    failures = []

    wc = env["mrp.workcenter"].search([("name", "=", WORKCENTER_NAME)], limit=1)
    if not wc:
        return [f"Work Center '{WORKCENTER_NAME}' not found"]
    if not wc.active:
        failures.append("Work Center is archived, expected active")

    prod = env["product.product"].search(
        [("name", "=", PRODUCT_NAME)], limit=1
    )
    if not prod:
        return [f"Product '{PRODUCT_NAME}' not found"]

    bom = env["mrp.bom"].search(
        [("product_tmpl_id", "=", prod.product_tmpl_id.id)], limit=1
    )
    if not bom:
        return [f"BOM for '{PRODUCT_NAME}' not found"]

    ops = bom.operation_ids
    if len(ops) != 1:
        failures.append(
            f"BOM has {len(ops)} operations, expected 1"
        )
    else:
        op = ops[0]
        if op.name != "Final Assembly":
            failures.append(
                f"Operation name is '{op.name}', expected 'Final Assembly'"
            )
        if op.workcenter_id.id != wc.id:
            failures.append(
                f"Operation work center is '{op.workcenter_id.name}', "
                f"expected '{WORKCENTER_NAME}'"
            )
        if abs(op.time_cycle_manual - 30.0) > 0.5:
            failures.append(
                f"Operation time_cycle_manual is {op.time_cycle_manual}, "
                f"expected ~30"
            )

    # Existing 2 components must remain untouched
    if len(bom.bom_line_ids) != 2:
        failures.append(
            f"BOM has {len(bom.bom_line_ids)} components, expected 2 "
            f"(seeded components must not be modified)"
        )

    return failures
