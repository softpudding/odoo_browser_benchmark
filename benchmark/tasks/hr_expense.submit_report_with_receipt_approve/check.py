"""Postcondition checks for hr_expense.submit_report_with_receipt_approve."""


def check(env):
    failures = []
    expenses = env["hr.expense"].search([
        ("name", "=", "Harbor Summit Hotel"),
        ("employee_id.name", "=", "Administrator"),
    ])
    if len(expenses) != 1:
        return [f"Expected exactly 1 target expense, found {len(expenses)}"]

    expense = expenses[0]
    if expense.product_id.name != "[HOTEL] Hotel Stay":
        failures.append(f"Expense category is {expense.product_id.name!r}")
    if expense.state != "approved":
        failures.append(f"Expense state is {expense.state!r}, expected 'approved'")
    if str(expense.date) != "2026-04-08":
        failures.append(f"Expense date is {expense.date!s}, expected 2026-04-08")
    if round(expense.total_amount_currency, 2) != 486.75:
        failures.append(
            f"Expense total is {expense.total_amount_currency}, expected 486.75"
        )
    if not expense.attachment_ids:
        failures.append("Expense has no attached receipt")
    return failures
