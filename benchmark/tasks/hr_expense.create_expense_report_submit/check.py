"""Postcondition checks for hr_expense.create_expense_report_submit.

Validates:
1. An expense exists with description "Hotel stay - Berlin conference".
2. Total amount is 385.00.
3. State is "submitted" (or "reported").
4. Expense date is June 15, 2026.
"""

from datetime import date


def check(env):
    failures = []

    expenses = env["hr.expense"].search([
        ("name", "=", "Hotel stay - Berlin conference"),
    ])
    if not expenses:
        return ["No expense found with description 'Hotel stay - Berlin conference'"]
    if len(expenses) > 1:
        failures.append(f"Found {len(expenses)} expenses, expected 1")

    expense = expenses[0]

    # State should be submitted (or approved if auto-approved by manager)
    if expense.state not in ("submitted", "reported", "approved"):
        failures.append(
            f"Expense state is '{expense.state}', expected 'submitted' or 'approved'"
        )

    # Check total amount
    amount = expense.total_amount_currency or expense.total_amount
    if abs(amount - 385.0) > 0.01:
        failures.append(f"Expense amount is {amount}, expected 385.00")

    # Check date
    if expense.date != date(2026, 6, 15):
        failures.append(f"Expense date is {expense.date}, expected 2026-06-15")

    # Check payment mode
    if expense.payment_mode != "own_account":
        failures.append(
            f"Payment mode is '{expense.payment_mode}', expected 'own_account'"
        )

    return failures
