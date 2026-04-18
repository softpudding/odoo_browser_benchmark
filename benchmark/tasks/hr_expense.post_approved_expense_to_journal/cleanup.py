"""Cleanup for hr_expense.post_approved_expense_to_journal."""

EXPENSE_NAME = "Bench Taxi Fare"
PRODUCT_NAME = "Benchmark Taxi Transportation"
EMPLOYEE_NAME = "Dana Silverstein"


def cleanup(env):
    Expense = env["hr.expense"]

    stale = Expense.search([("name", "=", EXPENSE_NAME)])
    for e in stale:
        # Reset if possible so linked moves can be reversed/unlinked.
        if e.state != "draft":
            try:
                e.action_reset()
            except Exception:
                pass
        moves = e.sudo().account_move_id
        for m in moves:
            try:
                if m.state == "posted":
                    m.button_draft()
                m.sudo().unlink()
            except Exception:
                pass
    stale.unlink()

    # Clean up product template and employee seeded by this task.
    env["product.template"].search(
        [("name", "=", PRODUCT_NAME)]
    ).unlink()
    env["hr.employee"].search(
        [("name", "=", EMPLOYEE_NAME)]
    ).unlink()
