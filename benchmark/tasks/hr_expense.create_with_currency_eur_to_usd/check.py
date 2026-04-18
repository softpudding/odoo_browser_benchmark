"""Postcondition checks for hr_expense.create_with_currency_eur_to_usd.

Validates:
- A draft hr.expense named 'NYC Hotel' exists.
- Category is 'Hotel'.
- Currency is EUR (not the default USD).
- total_amount_currency == 185.00 (in EUR).
- total_amount converted to ~200.00 USD via the seeded rate (0.925).
- payment_mode is 'own_account' (Employee).
- Date is 2026-04-01.
"""

from datetime import date


def check(env):
    failures = []

    expenses = env["hr.expense"].search([("name", "=", "NYC Hotel")])
    if not expenses:
        return ["No expense found with description 'NYC Hotel'"]
    if len(expenses) > 1:
        failures.append(f"Found {len(expenses)} expenses named 'NYC Hotel', expected exactly 1")

    expense = expenses[0]

    if expense.state != "draft":
        failures.append(f"Expense state is {expense.state!r}, expected 'draft'")

    if expense.payment_mode != "own_account":
        failures.append(
            f"payment_mode is {expense.payment_mode!r}, expected 'own_account' (Employee)"
        )

    if expense.product_id.name != "Hotel":
        failures.append(
            f"Category is {expense.product_id.name!r}, expected 'Hotel'"
        )

    if expense.currency_id.name != "EUR":
        failures.append(
            f"Expense currency is {expense.currency_id.name!r}, expected 'EUR'"
        )

    if abs(expense.total_amount_currency - 185.00) > 0.01:
        failures.append(
            f"total_amount_currency is {expense.total_amount_currency}, expected 185.00 (EUR)"
        )

    # Converted to USD via rate 0.925 -> 200.00 USD; allow small FP/rounding tolerance.
    if abs(expense.total_amount - 200.00) > 0.50:
        failures.append(
            f"total_amount (USD) is {expense.total_amount}, expected ~200.00 (185 EUR / 0.925)"
        )

    if expense.date != date(2026, 4, 1):
        failures.append(f"Expense date is {expense.date}, expected 2026-04-01")

    return failures
