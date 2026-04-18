"""Postcondition checks for mrp.plan_workorder_block_resume_finish_mo."""


def check(env):
    failures = []

    mo = env["mrp.production"].search([("name", "=", "WH/MO/BENCH-WO-01")], limit=1)
    if not mo:
        return ["Manufacturing order 'WH/MO/BENCH-WO-01' not found"]

    if mo.state != "done":
        failures.append(f"MO state is '{mo.state}', expected 'done'")
    if len(mo.workorder_ids) != 1:
        failures.append(f"Expected exactly 1 work order, found {len(mo.workorder_ids)}")
        return failures

    wo = mo.workorder_ids[0]
    if wo.state != "done":
        failures.append(f"Work order state is '{wo.state}', expected 'done'")
    if not wo.date_start or not wo.date_finished:
        failures.append("Work order is missing start or finish timestamps")

    block_entries = env["mrp.workcenter.productivity"].search([
        ("workcenter_id", "=", wo.workcenter_id.id),
        ("loss_id.name", "=", "Equipment Failure"),
    ])
    if not block_entries:
        failures.append("No 'Equipment Failure' block entry was recorded on the work center")
    elif any(not entry.date_end for entry in block_entries):
        failures.append("Work center is still blocked after the task")

    return failures
