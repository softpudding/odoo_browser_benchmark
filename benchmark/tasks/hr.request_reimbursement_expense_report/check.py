"""Postcondition checks for hr.request_reimbursement_expense_report.

Validates:
  - Exactly one hr.expense with name 'Bench Travel Expense'.
  - state == 'posted' (Submit → Approve → Post Journal Entries all done).
  - approval_state == 'approved' (canonical approval flag for v19).
  - total_amount == 150.00, unchanged by the agent.
  - employee_id is admin's hr.employee (agent must not pick a distractor).
  - product_id.display_name == 'Bench Travel Service'.
  - payment_mode == 'own_account' (Employee-to-reimburse).
  - account_move_id is set and that move is posted.
  - No extra `Bench Travel Expense` records were created.
"""


EXPENSE_NAME = "Bench Travel Expense"
PRODUCT_NAME = "Bench Travel Service"


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

    if expense.state != "posted":
        failures.append(
            f"Expense state is '{expense.state}' (approval_state="
            f"'{expense.approval_state}'), expected 'posted' — the agent must "
            "Submit, Approve, AND Post Journal Entries."
        )

    if expense.approval_state != "approved":
        failures.append(
            f"Expense approval_state is '{expense.approval_state}', expected 'approved'."
        )

    if abs(expense.total_amount - 150.0) > 0.01:
        failures.append(
            f"Expense total_amount is {expense.total_amount}, expected 150.00 "
            "(agent should not have changed the amount)."
        )

    if expense.product_id.display_name != PRODUCT_NAME:
        failures.append(
            f"Expense product is '{expense.product_id.display_name}', expected "
            f"'{PRODUCT_NAME}' (agent should not have changed the product)."
        )

    if expense.payment_mode != "own_account":
        failures.append(
            f"Expense payment_mode is '{expense.payment_mode}', expected "
            "'own_account' (Employee to reimburse)."
        )

    admin = env.ref("base.user_admin")
    admin_emp = env["hr.employee"].search([("user_id", "=", admin.id)], limit=1)
    if admin_emp and expense.employee_id.id != admin_emp.id:
        failures.append(
            f"Expense employee is '{expense.employee_id.display_name}', "
            f"expected admin's employee '{admin_emp.display_name}'."
        )

    move = expense.account_move_id
    if not move:
        failures.append(
            "Expense has no account_move_id — Post Journal Entries was not completed."
        )
    else:
        if move.state != "posted":
            failures.append(
                f"account.move for the expense is in state '{move.state}', "
                "expected 'posted'."
            )

    return failures
