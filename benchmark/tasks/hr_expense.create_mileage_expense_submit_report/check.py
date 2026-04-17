"""Postcondition checks for hr_expense.create_mileage_expense_submit_report."""


def check(env):
    failures = []
    expenses = env["hr.expense"].search([
        ("name", "=", "Client Visit Mileage"),
        ("employee_id.name", "=", "Administrator"),
    ])
    if len(expenses) != 1:
        return [f"Expected exactly 1 target expense, found {len(expenses)}"]

    expense = expenses[0]
    if "Mileage" not in expense.product_id.display_name:
        failures.append(f"Expense category is {expense.product_id.name!r}")
    if expense.state != "submitted":
        failures.append(f"Expense state is {expense.state!r}, expected 'submitted'")
    if str(expense.date) != "2026-04-14":
        failures.append(f"Expense date is {expense.date!s}, expected 2026-04-14")
    if round(expense.total_amount_currency, 2) != 128.40:
        failures.append(
            f"Expense total is {expense.total_amount_currency}, expected 128.40"
        )
    return failures
