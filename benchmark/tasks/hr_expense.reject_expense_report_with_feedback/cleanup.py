"""Cleanup for hr_expense.reject_expense_report_with_feedback."""

EXPENSE_NAME = "SUMMIT-2026 — overpriced hotel night"
PRODUCT_NAME = "Benchmark Hotel Over-cap"
EMPLOYEE_NAME = "Alice Benchmark"


def cleanup(env):
    env["hr.expense"].search([("name", "=", EXPENSE_NAME)]).unlink()
    env["product.template"].search([("name", "=", PRODUCT_NAME)]).unlink()
    env["hr.employee"].search([("name", "=", EMPLOYEE_NAME)]).unlink()
