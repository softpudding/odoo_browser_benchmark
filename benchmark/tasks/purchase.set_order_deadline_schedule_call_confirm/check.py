"""Postcondition checks for purchase.set_order_deadline_schedule_call_confirm."""

from datetime import date, datetime


def check(env):
    failures = []

    vendor = env["res.partner"].search(
        [("name", "=", "Blue Peak Industrial")],
        limit=1,
    )
    if not vendor:
        return ["Vendor 'Blue Peak Industrial' not found"]

    po = env["purchase.order"].search([
        ("partner_id", "=", vendor.id),
        ("partner_ref", "=", "MED-RFQ-ACT-01"),
    ], limit=1)
    if not po:
        return ["Target RFQ 'MED-RFQ-ACT-01' not found"]

    if po.state != "purchase":
        failures.append(f"PO state is '{po.state}', expected 'purchase'")

    actual_date = po.date_order.date() if isinstance(po.date_order, datetime) else po.date_order
    if actual_date != date(2026, 5, 21):
        failures.append(
            f"Order deadline is {actual_date}, expected 2026-05-21"
        )

    activities = env["mail.activity"].search([
        ("res_model", "=", "purchase.order"),
        ("res_id", "=", po.id),
        ("summary", "=", "Confirm dock appointment"),
    ])
    if not activities:
        failures.append("Expected Call activity was not scheduled on the PO")
    else:
        activity = activities[0]
        if activity.activity_type_id.name != "Call":
            failures.append(
                f"Activity type is '{activity.activity_type_id.name}', expected 'Call'"
            )
        if activity.date_deadline != date(2026, 5, 18):
            failures.append(
                f"Activity due date is {activity.date_deadline}, expected 2026-05-18"
            )

    if len(po.order_line) != 2:
        failures.append(f"Expected 2 PO lines, found {len(po.order_line)}")

    dock_plate = po.order_line.filtered(lambda line: line.product_id.name == "Dock Plate")
    tape = po.order_line.filtered(lambda line: line.product_id.name == "Packing Tape Case")
    if not dock_plate or dock_plate.product_qty != 8:
        failures.append("Dock Plate line was changed unexpectedly")
    if not tape or tape.product_qty != 12:
        failures.append("Packing Tape Case line was changed unexpectedly")

    distractor = env["purchase.order"].search([
        ("partner_id", "=", vendor.id),
        ("partner_ref", "=", "MED-RFQ-ACT-02"),
    ], limit=1)
    if not distractor:
        failures.append("Distractor RFQ 'MED-RFQ-ACT-02' not found")
    else:
        if distractor.state != "draft":
            failures.append(
                f"Distractor RFQ state is '{distractor.state}', expected 'draft'"
            )
        if env["mail.activity"].search_count([
            ("res_model", "=", "purchase.order"),
            ("res_id", "=", distractor.id),
            ("summary", "=", "Confirm dock appointment"),
        ]):
            failures.append("Distractor RFQ received the target activity")

    return failures
