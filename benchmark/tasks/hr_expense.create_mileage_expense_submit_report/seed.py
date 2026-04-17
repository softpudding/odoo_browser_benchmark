"""Seed data for hr_expense.create_mileage_expense_submit_report."""


EXPENSE_NAME = "Client Visit Mileage"
EMPLOYEE_NAME = "Administrator"
PRODUCT_NAME = "Mileage"


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

    product = env.ref("hr_expense.expense_product_mileage", raise_if_not_found=False)
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
