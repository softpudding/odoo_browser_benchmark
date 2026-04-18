"""Postcondition checks for hr_holidays.refuse_then_re_request_other_type."""

from datetime import date

REASON_BODY = "Use sick leave instead"


def check(env):
    failures = []

    # ------------------------------------------------------------------
    # 1. Original Paid Time Off leave must exist and be refused.
    # ------------------------------------------------------------------
    originals = env["hr.leave"].with_context(active_test=False).search([
        ("name", "=", "Family vacation"),
    ])
    if not originals:
        return ["No original leave with description 'Family vacation' found"]
    if len(originals) > 1:
        failures.append(
            f"Found {len(originals)} 'Family vacation' leaves, expected 1"
        )
    original = originals[0]

    if original.state != "refuse":
        failures.append(
            f"Original leave state is '{original.state}', expected 'refuse'"
        )
    if original.holiday_status_id.name != "Paid Time Off":
        failures.append(
            f"Original leave type is '{original.holiday_status_id.name}', "
            "expected 'Paid Time Off'"
        )
    if original.employee_id.name != "Eve Employee":
        failures.append(
            f"Original leave employee is '{original.employee_id.name}', "
            "expected 'Eve Employee'"
        )

    # ------------------------------------------------------------------
    # 2. Refusal reason chatter message exists on the original.
    # ------------------------------------------------------------------
    messages = env["mail.message"].search([
        ("model", "=", "hr.leave"),
        ("res_id", "=", original.id),
    ])
    found_reason = False
    for msg in messages:
        body = msg.body or ""
        import re
        text = re.sub(r"<[^>]+>", " ", body)
        text = re.sub(r"\s+", " ", text).strip()
        if REASON_BODY in text:
            found_reason = True
            break
    if not found_reason:
        failures.append(
            f"No chatter message containing '{REASON_BODY}' on the refused "
            "Paid Time Off leave"
        )

    # ------------------------------------------------------------------
    # 3. New Sick Time Off leave for Eve, same dates, in 'confirm'.
    # ------------------------------------------------------------------
    eve_employee = env["hr.employee"].search(
        [("name", "=", "Eve Employee")], limit=1
    )
    if not eve_employee:
        failures.append("Eve Employee record not found")
        return failures

    sick_type = env["hr.leave.type"].search(
        [("name", "=", "Sick Time Off")], limit=1
    )
    if not sick_type:
        failures.append("Sick Time Off leave type not found")
        return failures

    new_leaves = env["hr.leave"].with_context(active_test=False).search([
        ("employee_id", "=", eve_employee.id),
        ("holiday_status_id", "=", sick_type.id),
    ])
    if not new_leaves:
        failures.append(
            "No Sick Time Off leave for Eve Employee found (re-request "
            "step missing)"
        )
        return failures

    # Among possibly-multiple sick leaves, the new one is whichever covers
    # 2026-08-10..2026-08-12.
    target = None
    for lv in new_leaves:
        from_d = lv.date_from.date() if lv.date_from else None
        to_d = lv.date_to.date() if lv.date_to else None
        if from_d == date(2026, 8, 10) and to_d == date(2026, 8, 12):
            target = lv
            break
    if not target:
        failures.append(
            "No Sick Time Off leave for Eve covering 2026-08-10 to "
            "2026-08-12 found"
        )
        return failures

    if target.state not in ("confirm", "validate1"):
        failures.append(
            f"New Sick Time Off leave state is '{target.state}', "
            "expected 'confirm' (To Approve)"
        )
    if target.state == "validate":
        failures.append(
            "New Sick Time Off leave was approved; should remain in "
            "'To Approve' state"
        )
    if abs(target.number_of_days - 3.0) > 0.01:
        failures.append(
            f"New Sick Time Off leave number_of_days is {target.number_of_days}, "
            "expected 3.0"
        )

    return failures
