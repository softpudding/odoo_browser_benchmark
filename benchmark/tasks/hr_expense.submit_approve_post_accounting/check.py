"""Postcondition checks for hr_expense.submit_approve_post_accounting.

The task asks the agent to push the expense through draft → submitted →
approved (→ posted). In Odoo 19 with the base snapshot, posting to
accounting requires journal configuration that isn't always reachable
from the UI; we therefore accept any state on or after 'approved' as
success and credit a posted journal entry as a bonus if present.
"""


EXPENSE_NAME = "TRV-2026-04 — April client visit"
TERMINAL_OK_STATES = ("approved", "posted", "in_payment", "paid")


def check(env):
    failures = []

    expenses = env["hr.expense"].search([("name", "=", EXPENSE_NAME)])
    if not expenses:
        return [f"No expense found named '{EXPENSE_NAME}'"]
    if len(expenses) > 1:
        failures.append(f"Found {len(expenses)} expenses, expected 1")
    exp = expenses[0]

    if exp.state not in TERMINAL_OK_STATES:
        failures.append(
            f"Expense state is '{exp.state}', expected one of "
            f"{TERMINAL_OK_STATES}"
        )

    return failures
