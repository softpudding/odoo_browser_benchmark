"""Cleanup for hr_expense.reject_expense_report_with_feedback."""

REPORT_NAME = "SUMMIT-2026 – Summit trip reimbursement"
EXPENSE_NAME = "Overpriced hotel night"
PRODUCT_NAME = "Benchmark Hotel Over-cap"
EMPLOYEE_NAME = "Alice Benchmark"


def cleanup(env):
    sheets = env["hr.expense.sheet"].search([("name", "=", REPORT_NAME)])
    for sheet in sheets:
        try:
            sheet.action_reset_expense_sheets()
        except Exception:
            pass
    for sheet in sheets:
        sheet.expense_line_ids.unlink()
        sheet.unlink()
    env["hr.expense"].search([("name", "=", EXPENSE_NAME)]).unlink()
    env["product.template"].search([("name", "=", PRODUCT_NAME)]).unlink()
    env["hr.employee"].search([("name", "=", EMPLOYEE_NAME)]).unlink()
