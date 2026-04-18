"""Postcondition checks for hr_expense.refuse_report_with_reason_chatter."""


EXPENSE_NAME = "INVOICE-MISMATCH-2026 — duplicate receipt"
EXPECTED_REASON_SNIPPET = "Receipt amount doesn't match invoice"


def check(env):
    failures = []

    expenses = env["hr.expense"].search([("name", "=", EXPENSE_NAME)])
    if not expenses:
        return [f"No expense found named '{EXPENSE_NAME}'"]
    if len(expenses) > 1:
        failures.append(
            f"Found {len(expenses)} expenses named '{EXPENSE_NAME}', "
            f"expected 1"
        )
    exp = expenses[0]

    if exp.state != "refused":
        failures.append(
            f"Expense state is '{exp.state}', expected 'refused'"
        )

    messages = exp.message_ids
    bodies = " ".join((m.body or "") for m in messages)
    # Strip HTML tags cheaply for substring checks.
    import re as _re
    plain = _re.sub(r"<[^>]+>", " ", bodies)
    # Normalize curly apostrophes.
    plain = plain.replace("\u2019", "'")
    if EXPECTED_REASON_SNIPPET.lower() not in plain.lower():
        failures.append(
            f"Refusal reason '{EXPECTED_REASON_SNIPPET}' not found in "
            f"expense chatter"
        )

    return failures
