"""Postcondition checks for hr_expense.scan_submit_expense_from_mobile_portal.

Validates:
  - Exactly one hr.expense with name 'Airport taxi' exists.
  - total_amount == 45.00 (agent overrode the 25.00 default).
  - product_id refers to 'Travel - Taxi'.
  - state is in ('reported','submitted','approved') — i.e., the expense
    left 'draft'. Odoo 19 uses 'submitted' on the approval_state; the
    computed state may surface as 'submitted' or 'approved'.
  - The expense is owned by admin's hr.employee (not a different employee).
"""


PRODUCT_NAME = "Travel - Taxi"
EXPENSE_NAME = "Airport taxi"
ACCEPTABLE_STATES = {"reported", "submitted", "approved"}


def check(env):
    failures = []

    expenses = env["hr.expense"].search([("name", "=", EXPENSE_NAME)])
    if len(expenses) == 0:
        return [f"No hr.expense named '{EXPENSE_NAME}' found"]
    if len(expenses) > 1:
        failures.append(
            f"Expected exactly 1 expense named '{EXPENSE_NAME}', found {len(expenses)}"
        )

    expense = expenses[0]

    if expense.product_id.display_name != PRODUCT_NAME:
        failures.append(
            f"Expense product is '{expense.product_id.display_name}', expected '{PRODUCT_NAME}'"
        )

    if abs(expense.total_amount - 45.0) > 0.01:
        failures.append(
            f"Expense total_amount is {expense.total_amount}, expected 45.00 "
            "— agent must override the default 25.00"
        )

    if expense.state not in ACCEPTABLE_STATES:
        failures.append(
            f"Expense state is '{expense.state}' (approval_state="
            f"'{expense.approval_state}'), expected one of {sorted(ACCEPTABLE_STATES)}"
        )

    admin = env.ref("base.user_admin")
    admin_emp = env["hr.employee"].search([("user_id", "=", admin.id)], limit=1)
    if admin_emp and expense.employee_id.id != admin_emp.id:
        failures.append(
            f"Expense employee is '{expense.employee_id.display_name}', "
            f"expected admin's employee '{admin_emp.display_name}'"
        )

    return failures
