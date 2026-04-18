"""Postcondition checks for hr_expense.submit_report_for_approval."""


EXPENSE_NAME = "Hotel in Paris"
PRODUCT_NAME = "Travel & Accommodation"


def check(env):
    failures = []

    expenses = env["hr.expense"].search([("name", "=", EXPENSE_NAME)])
    if len(expenses) != 1:
        return [
            f"Expected exactly 1 expense named '{EXPENSE_NAME}', found {len(expenses)}"
        ]

    expense = expenses[0]

    if expense.employee_id.display_name != "Administrator":
        failures.append(
            f"Expense employee is '{expense.employee_id.display_name}', expected 'Administrator'"
        )
    # The product is shown with its internal reference prefix in display_name
    # (e.g. "[TRANS & ACC] Travel & Accommodation"). Match on product name
    # rather than display_name.
    if expense.product_id.name != PRODUCT_NAME:
        failures.append(
            f"Expense category is '{expense.product_id.name}', expected '{PRODUCT_NAME}'"
        )
    if abs(expense.total_amount - 250.0) > 0.0001:
        failures.append(
            f"Expense total is {expense.total_amount}, expected 250.0"
        )
    if str(expense.date) != "2026-03-12":
        failures.append(
            f"Expense date is '{expense.date}', expected '2026-03-12'"
        )
    # Accept 'submitted' or later workflow states (approved/posted) because
    # the task only requires Submit to Manager, but a faster agent might
    # continue further. 'draft' and 'refused' are failures.
    if expense.state not in {"submitted", "approved", "posted", "in_payment", "paid"}:
        failures.append(
            f"Expense state is '{expense.state}', expected 'submitted' (or a later approval state)"
        )

    return failures
