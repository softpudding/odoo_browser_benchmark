"""Seed for hr_expense.reject_expense_report_with_feedback.

Odoo 19 uses hr.expense directly (no hr.expense.sheet). Creates a
submitted expense for Alice Benchmark that the approver must refuse.
"""

EMPLOYEE_NAME = "Alice Benchmark"
PRODUCT_NAME = "Benchmark Hotel Over-cap"
EXPENSE_NAME = "SUMMIT-2026 — overpriced hotel night"


def setup(env):
    admin = env.ref("base.user_admin")

    # Cleanup prior runs.
    env["hr.expense"].search([("name", "=", EXPENSE_NAME)]).unlink()

    emp = env["hr.employee"].search([("name", "=", EMPLOYEE_NAME)], limit=1)
    if not emp:
        emp = env["hr.employee"].create({
            "name": EMPLOYEE_NAME,
            "work_email": "alice.benchmark@example.com",
            "expense_manager_id": admin.id,
        })
    else:
        emp.write({"expense_manager_id": admin.id})

    products = env["product.template"].search([("name", "=", PRODUCT_NAME)])
    if not products:
        tmpl = env["product.template"].create({
            "name": PRODUCT_NAME,
            "type": "service",
            "purchase_ok": True,
            "sale_ok": False,
            "can_be_expensed": True,
            "list_price": 320.0,
        })
        product = tmpl.product_variant_id
    else:
        product = products[0].product_variant_id

    expense = env["hr.expense"].create({
        "name": EXPENSE_NAME,
        "employee_id": emp.id,
        "product_id": product.id,
        "total_amount": 320.0,
        "quantity": 1.0,
        "date": "2026-05-02",
    })

    # Submit so it lands in the approver queue.
    try:
        expense.action_submit()
    except Exception:
        pass

    # Admin needs expense approval rights.
    for grp_ref in [
        "hr_expense.group_hr_expense_team_approver",
        "hr_expense.group_hr_expense_manager",
        "hr_expense.group_hr_expense_user",
    ]:
        group = env.ref(grp_ref, raise_if_not_found=False)
        if group and group not in admin.group_ids:
            admin.write({"group_ids": [(4, group.id)]})
