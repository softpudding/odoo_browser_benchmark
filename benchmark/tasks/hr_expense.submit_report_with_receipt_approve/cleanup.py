"""Cleanup for hr_expense.submit_report_with_receipt_approve."""

from pathlib import Path


def cleanup(env):
    expenses = env["hr.expense"].search([("name", "=", "Harbor Summit Hotel")])
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
    Path("/tmp/hr_expense_submit_report_with_receipt_approve.svg").unlink(missing_ok=True)
