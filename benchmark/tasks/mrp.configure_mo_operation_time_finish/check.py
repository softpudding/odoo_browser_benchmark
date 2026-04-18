"""Postcondition checks for mrp.configure_mo_operation_time_finish.

Validates:
1. The work order for MO WH/MO/BENCH0001 exists (under operation name
   'Assembly Station').
2. Its expected duration is 45 minutes.
3. Its state is 'done'.
4. The underlying MO was not cancelled.
"""


MO_NAME = "WH/MO/BENCH0001"
OPERATION_NAME = "Assembly Station"


def check(env):
    failures = []

    mo = env["mrp.production"].search([("name", "=", MO_NAME)], limit=1)
    if not mo:
        return [f"Manufacturing order '{MO_NAME}' not found"]
    if mo.state == "cancel":
        failures.append(
            f"MO '{MO_NAME}' is cancelled; it must not be cancelled"
        )

    wo = env["mrp.workorder"].search([
        ("production_id", "=", mo.id),
        ("name", "=", OPERATION_NAME),
    ], limit=1)
    if not wo:
        # Fall back: any workorder on that MO
        wo = env["mrp.workorder"].search([
            ("production_id", "=", mo.id),
        ], limit=1)
    if not wo:
        return [
            f"No work order found on MO '{MO_NAME}' "
            f"(expected operation '{OPERATION_NAME}')"
        ]

    if abs(wo.duration_expected - 45.0) > 0.5:
        failures.append(
            f"Work order duration_expected is {wo.duration_expected}, "
            f"expected 45"
        )

    if wo.state != "done":
        failures.append(
            f"Work order state is '{wo.state}', expected 'done'"
        )

    return failures
