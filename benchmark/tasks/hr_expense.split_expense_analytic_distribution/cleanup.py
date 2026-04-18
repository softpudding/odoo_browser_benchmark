"""Cleanup for hr_expense.split_expense_analytic_distribution."""

EXPENSE_NAME = "Bench Split Travel"
PRODUCT_NAME = "Benchmark Travel Split"
EMPLOYEE_NAME = "Morgan Pearce"
PLAN_NAME = "Bench Plan"
ALPHA_NAME = "Bench Project Alpha"
BETA_NAME = "Bench Project Beta"


def cleanup(env):
    Expense = env["hr.expense"]

    stale = Expense.search([("name", "=", EXPENSE_NAME)])
    for e in stale:
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

    # Remove the analytic accounts + plan created for this task.
    env["account.analytic.account"].search([
        ("name", "in", [ALPHA_NAME, BETA_NAME]),
    ]).unlink()
    env["account.analytic.plan"].search([
        ("name", "=", PLAN_NAME),
    ]).unlink()

    # Product template + employee.
    env["product.template"].search(
        [("name", "=", PRODUCT_NAME)]
    ).unlink()
    env["hr.employee"].search(
        [("name", "=", EMPLOYEE_NAME)]
    ).unlink()
