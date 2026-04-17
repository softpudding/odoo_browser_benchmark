"""Cleanup for hr_expense.create_mileage_expense_submit_report."""


def cleanup(env):
    expenses = env["hr.expense"].search([("name", "=", "Client Visit Mileage")])
    for expense in expenses:
        attachments = env["ir.attachment"].search([
            ("res_model", "=", "hr.expense"),
            ("res_id", "=", expense.id),
        ])
        attachments.unlink()
        if expense.state != "draft":
            try:
                expense.action_reset()
            except Exception:
                pass
        expense.unlink()
