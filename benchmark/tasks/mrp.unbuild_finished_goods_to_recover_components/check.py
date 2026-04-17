"""Postcondition checks for mrp.unbuild_finished_goods_to_recover_components."""


MO_NAME = "WH/MO/UNBLD-001"
FINISHED = "Benchmark Recoverable Widget"


def check(env):
    failures = []

    mo = env["mrp.production"].search([("name", "=", MO_NAME)], limit=1)
    if not mo:
        return [f"Original MO '{MO_NAME}' not found"]
    if mo.state == "cancel":
        failures.append(
            f"MO {MO_NAME} is cancelled — it should remain in 'done' state"
        )

    unbuilds = env["mrp.unbuild"].search([("mo_id", "=", mo.id)])
    if not unbuilds:
        return failures + [
            f"No unbuild order linked to MO {MO_NAME} — the task requires "
            f"creating one"
        ]
    if len(unbuilds) > 1:
        failures.append(
            f"Expected exactly 1 unbuild on MO {MO_NAME}, found {len(unbuilds)}"
        )
    u = unbuilds[0]

    if u.state != "done":
        failures.append(
            f"Unbuild state is '{u.state}', expected 'done' (validated)"
        )
    if u.product_id.name != FINISHED:
        failures.append(
            f"Unbuild product is '{u.product_id.name}', expected '{FINISHED}'"
        )
    if abs((u.product_qty or 0.0) - 3.0) > 1e-6:
        failures.append(
            f"Unbuild quantity is {u.product_qty}, expected 3"
        )

    return failures
