"""Cleanup for hr_expense.submit_report_for_approval."""


EXPENSE_NAME = "Hotel in Paris"


def cleanup(env):
    expenses = env["hr.expense"].search([("name", "=", EXPENSE_NAME)])
    for expense in expenses:
        move = getattr(expense, "account_move_id", None)
        if move and move.state == "posted":
            try:
                move.button_draft()
            except Exception:
                pass
        if move:
            try:
                move.unlink()
            except Exception:
                pass
        if expense.state != "draft":
            try:
                expense.action_reset()
            except Exception:
                pass
    expenses.unlink()
