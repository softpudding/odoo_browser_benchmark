"""Postcondition checks for hr_expense.create_expense_report_submit."""


PRODUCT_NAME = "Hotel Stay"
EXPENSE_NAME = "Summit hotel stay"


def check(env):
    failures = []

    expenses = env["hr.expense"].search([("name", "=", EXPENSE_NAME)])
    if len(expenses) != 1:
        return [f"Expected exactly 1 expense named '{EXPENSE_NAME}', found {len(expenses)}"]

    expense = expenses[0]
    if expense.employee_id.display_name != "Administrator":
        failures.append(
            f"Expense employee is '{expense.employee_id.display_name}', expected 'Administrator'"
        )
    if expense.product_id.display_name != PRODUCT_NAME:
        failures.append(
            f"Expense category is '{expense.product_id.display_name}', expected '{PRODUCT_NAME}'"
        )
    if abs(expense.total_amount - 245.0) > 0.0001:
        failures.append(f"Expense total is {expense.total_amount}, expected 245.0")
    if str(expense.date) != "2026-07-02":
        failures.append(f"Expense date is '{expense.date}', expected '2026-07-02'")
    if expense.state not in {"submitted", "approved"}:
        failures.append(
            f"Expense state is '{expense.state}', expected 'submitted' or 'approved'"
        )

    return failures
