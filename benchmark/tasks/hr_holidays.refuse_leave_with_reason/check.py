"""Postcondition checks for hr_holidays.refuse_leave_with_reason."""

REQUIRED_BODY = "Denied: conflicts with critical project deadline"


def check(env):
    failures = []

    leaves = env["hr.leave"].with_context(active_test=False).search([
        ("name", "=", "Personal emergency"),
    ])
    if not leaves:
        return ["No leave request found with description 'Personal emergency'"]
    leave = leaves[0]

    if leave.state != "refuse":
        failures.append(f"Leave state is '{leave.state}', expected 'refuse'")

    messages = env["mail.message"].search([
        ("model", "=", "hr.leave"),
        ("res_id", "=", leave.id),
    ])
    found = False
    for msg in messages:
        plain = (msg.body or "")
        # mail.message body is HTML; strip tags to compare text
        import re
        text = re.sub(r"<[^>]+>", " ", plain)
        text = re.sub(r"\s+", " ", text).strip()
        if REQUIRED_BODY in text:
            found = True
            break
    if not found:
        failures.append(
            f"No chatter message with reason text "
            f"'{REQUIRED_BODY}' on the refused leave"
        )

    return failures
