"""Cleanup for hr_expense.submit_approve_post_accounting."""

EXPENSE_NAME = "TRV-2026-04 — April client visit"
PRODUCT_NAME = "Benchmark Client Travel"
EMPLOYEE_NAME = "Bob Benchmark"


def cleanup(env):
    expenses = env["hr.expense"].search([("name", "=", EXPENSE_NAME)])
    for e in expenses:
        try:
            move = getattr(e, "account_move_id", None)
            if move and move.state == "posted":
                move.button_draft()
            if move:
                move.unlink()
        except Exception:
            pass
    expenses.unlink()
    env["product.template"].search([("name", "=", PRODUCT_NAME)]).unlink()
    env["hr.employee"].search([("name", "=", EMPLOYEE_NAME)]).unlink()
