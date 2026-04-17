"""Seed data for hr_expense.submit_report_with_receipt_approve."""

from pathlib import Path


EXPENSE_NAME = "Harbor Summit Hotel"
EMPLOYEE_NAME = "Administrator"
PRODUCT_NAME = "[HOTEL] Hotel Stay"
RECEIPT_PATH = Path("/tmp/hr_expense_submit_report_with_receipt_approve.svg")


def _cleanup_expenses(env):
    expenses = env["hr.expense"].search([("name", "=", EXPENSE_NAME)])
    for expense in expenses:
        if expense.account_move_id and expense.account_move_id.state == "posted":
            expense.account_move_id.button_draft()
        if expense.state != "draft":
            try:
                expense.action_reset()
            except Exception:
                pass
        attachments = env["ir.attachment"].search([
            ("res_model", "=", "hr.expense"),
            ("res_id", "=", expense.id),
        ])
        attachments.unlink()
        expense.unlink()


def setup(env):
    _cleanup_expenses(env)

    admin = env.ref("base.user_admin")
    admin.group_ids |= env.ref("hr_expense.group_hr_expense_manager")

    employee = admin.employee_id
    if not employee:
        employee = env["hr.employee"].create({
            "name": EMPLOYEE_NAME,
            "work_email": "admin@example.com",
            "user_id": admin.id,
        })
    employee.expense_manager_id = admin

    product = env["product.product"].search([("name", "=", PRODUCT_NAME)], limit=1)
    if not product:
        tmpl = env["product.template"].create({
            "name": PRODUCT_NAME,
            "type": "service",
            "purchase_ok": True,
            "sale_ok": False,
            "can_be_expensed": True,
            "standard_price": 0.0,
            "list_price": 0.0,
        })
        product = tmpl.product_variant_id
    else:
        product.product_tmpl_id.write({
            "purchase_ok": True,
            "sale_ok": False,
            "can_be_expensed": True,
            "standard_price": 0.0,
            "list_price": 0.0,
        })

    RECEIPT_PATH.write_text(
        "<svg xmlns='http://www.w3.org/2000/svg' width='320' height='200'>"
        "<rect width='100%' height='100%' fill='#f8fafc'/>"
        "<text x='18' y='48' font-size='18'>Harbor Summit Hotel</text>"
        "<text x='18' y='84' font-size='14'>Date: 2026-04-08</text>"
        "<text x='18' y='116' font-size='14'>Total: 486.75</text>"
        "<text x='18' y='148' font-size='14'>Room and incidentals</text>"
        "</svg>"
    )
