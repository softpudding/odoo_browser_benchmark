"""Postcondition checks for hr_expense.reject_expense_report_with_feedback."""


REPORT_NAME = "SUMMIT-2026 – Summit trip reimbursement"
EXPECTED_REASON_SNIPPET = "Hotel rate exceeds company cap"


def check(env):
    failures = []

    sheets = env["hr.expense.sheet"].search([("name", "=", REPORT_NAME)])
    if not sheets:
        return [f"No expense report found named '{REPORT_NAME}'"]
    if len(sheets) > 1:
        failures.append(f"Found {len(sheets)} reports, expected 1")
    sheet = sheets[0]

    # A refused sheet is typically moved back to 'draft' with a chatter note,
    # or to 'cancel' depending on the version. Accept either non-approved
    # terminal state.
    if sheet.state not in ("draft", "cancel"):
        failures.append(
            f"Report state is '{sheet.state}', expected 'draft' or 'cancel' "
            f"(refused/not approved)"
        )

    # Verify the refusal reason was posted in chatter.
    messages = sheet.message_ids
    bodies = " ".join((m.body or "") for m in messages)
    if EXPECTED_REASON_SNIPPET.lower() not in bodies.lower():
        failures.append(
            f"Refusal reason '{EXPECTED_REASON_SNIPPET}' not found in report "
            f"chatter"
        )

    return failures
