"""Cleanup for hr_expense.create_expense_report_submit."""


def cleanup(env):
    env["hr.expense"].search([("name", "=", "Summit hotel stay")]).unlink()
    env["hr.employee"].search([("name", "=", "Benchmark Expense Admin")]).unlink()
    env["product.template"].search([("name", "=", "Hotel Stay")]).unlink()
