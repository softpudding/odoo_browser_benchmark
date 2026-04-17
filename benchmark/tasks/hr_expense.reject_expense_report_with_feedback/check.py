"""Postcondition checks for hr_expense.reject_expense_report_with_feedback."""


EXPENSE_NAME = "SUMMIT-2026 — overpriced hotel night"
EXPECTED_REASON_SNIPPET = "Hotel rate exceeds company cap"


def check(env):
    failures = []

    expenses = env["hr.expense"].search([("name", "=", EXPENSE_NAME)])
    if not expenses:
        return [f"No expense found named '{EXPENSE_NAME}'"]
    if len(expenses) > 1:
        failures.append(f"Found {len(expenses)} expenses, expected 1")
    exp = expenses[0]

    if exp.state != "refused":
        failures.append(
            f"Expense state is '{exp.state}', expected 'refused'"
        )

    messages = exp.message_ids
    bodies = " ".join((m.body or "") for m in messages)
    if EXPECTED_REASON_SNIPPET.lower() not in bodies.lower():
        failures.append(
            f"Refusal reason '{EXPECTED_REASON_SNIPPET}' not found in expense "
            f"chatter"
        )

    return failures
