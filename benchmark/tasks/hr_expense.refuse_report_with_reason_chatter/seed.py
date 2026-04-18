"""Seed for hr_expense.refuse_report_with_reason_chatter.

Odoo 19 unified hr.expense.sheet into hr.expense, so the "report" is
just an hr.expense record. Creates a single submitted expense for
Jordan Whitfield that the approver must refuse with a specific reason.
"""

EMPLOYEE_NAME = "Jordan Whitfield"
PRODUCT_NAME = "Benchmark Invoice Receipt Mismatch"
EXPENSE_NAME = "INVOICE-MISMATCH-2026 — duplicate receipt"


def setup(env):
    admin = env.ref("base.user_admin")

    # Cleanup prior runs.
    stale = env["hr.expense"].search([("name", "=", EXPENSE_NAME)])
    for e in stale:
        if e.state != "draft":
            try:
                e.action_reset()
            except Exception:
                pass
    stale.unlink()

    # Grant admin the required expense groups so they can approve/refuse.
    for grp_ref in [
        "hr_expense.group_hr_expense_team_approver",
        "hr_expense.group_hr_expense_manager",
        "hr_expense.group_hr_expense_user",
    ]:
        group = env.ref(grp_ref, raise_if_not_found=False)
        if group and group not in admin.group_ids:
            admin.write({"group_ids": [(4, group.id)]})

    # Ensure an employee; bind admin as expense manager so refuse is allowed.
    emp = env["hr.employee"].search(
        [("name", "=", EMPLOYEE_NAME)], limit=1
    )
    if not emp:
        emp = env["hr.employee"].create({
            "name": EMPLOYEE_NAME,
            "work_email": "jordan.whitfield@example.com",
            "expense_manager_id": admin.id,
        })
    else:
        emp.write({"expense_manager_id": admin.id})

    # Expense product.
    products = env["product.template"].search(
        [("name", "=", PRODUCT_NAME)]
    )
    if not products:
        tmpl = env["product.template"].create({
            "name": PRODUCT_NAME,
            "type": "service",
            "purchase_ok": True,
            "sale_ok": False,
            "can_be_expensed": True,
            "list_price": 275.0,
        })
        product = tmpl.product_variant_id
    else:
        product = products[0].product_variant_id

    # Create the expense "report" in submitted state.
    expense = env["hr.expense"].create({
        "name": EXPENSE_NAME,
        "employee_id": emp.id,
        "product_id": product.id,
        "total_amount_currency": 275.0,
        "quantity": 1.0,
        "date": "2026-04-05",
    })

    try:
        expense.action_submit()
    except Exception:
        pass
