"""Cleanup for hr_expense.refuse_report_with_reason_chatter."""

EXPENSE_NAME = "INVOICE-MISMATCH-2026 — duplicate receipt"
PRODUCT_NAME = "Benchmark Invoice Receipt Mismatch"
EMPLOYEE_NAME = "Jordan Whitfield"


def cleanup(env):
    env["hr.expense"].search([("name", "=", EXPENSE_NAME)]).unlink()
    env["product.template"].search([("name", "=", PRODUCT_NAME)]).unlink()
    env["hr.employee"].search([("name", "=", EMPLOYEE_NAME)]).unlink()
