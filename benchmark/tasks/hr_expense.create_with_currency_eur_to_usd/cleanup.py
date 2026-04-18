"""Cleanup for hr_expense.create_with_currency_eur_to_usd."""


def cleanup(env):
    expenses = env["hr.expense"].search([("name", "=", "NYC Hotel")])
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
