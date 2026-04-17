"""Cleanup for hr_expense.submit_approve_post_accounting."""

REPORT_NAME = "TRV-2026-04 – April client visit"
EXPENSE_NAME = "April client visit — train + meals"
PRODUCT_NAME = "Benchmark Client Travel"
EMPLOYEE_NAME = "Bob Benchmark"


def cleanup(env):
    sheets = env["hr.expense.sheet"].search([("name", "=", REPORT_NAME)])
    for sheet in sheets:
        try:
            moves = getattr(sheet, "account_move_ids", env["account.move"])
            moves.filtered(lambda m: m.state == "posted").button_draft()
            moves.unlink()
        except Exception:
            pass
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
