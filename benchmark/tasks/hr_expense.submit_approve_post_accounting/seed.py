"""Seed for hr_expense.submit_approve_post_accounting.

Category: closed_loop_cross_module (HARD).
Creates a draft expense report 'TRV-2026-04' for employee Bob Benchmark.
The task requires the agent to submit, approve, and post it to accounting.
"""

EMPLOYEE_NAME = "Bob Benchmark"
PRODUCT_NAME = "Benchmark Client Travel"
EXPENSE_NAME = "April client visit — train + meals"
REPORT_NAME = "TRV-2026-04 – April client visit"


def setup(env):
    admin = env.ref("base.user_admin")

    # Cleanup prior runs.
    prior_reports = env["hr.expense.sheet"].search([("name", "=", REPORT_NAME)])
    for sheet in prior_reports:
        try:
            sheet.account_move_ids.filtered(lambda m: m.state == "posted").button_draft()
        except Exception:
            pass
        try:
            sheet.account_move_ids.unlink()
        except Exception:
            pass
        try:
            sheet.action_reset_expense_sheets()
        except Exception:
            pass
    for sheet in prior_reports:
        sheet.expense_line_ids.unlink()
        sheet.unlink()
    env["hr.expense"].search([("name", "=", EXPENSE_NAME)]).unlink()

    emp = env["hr.employee"].search([("name", "=", EMPLOYEE_NAME)], limit=1)
    if not emp:
        emp = env["hr.employee"].create({
            "name": EMPLOYEE_NAME,
            "work_email": "bob.benchmark@example.com",
            "expense_manager_id": admin.id,
            "user_id": admin.id,
        })
    else:
        emp.write({
            "expense_manager_id": admin.id,
            "user_id": admin.id,
        })

    products = env["product.template"].search([("name", "=", PRODUCT_NAME)])
    if not products:
        tmpl = env["product.template"].create({
            "name": PRODUCT_NAME,
            "type": "service",
            "purchase_ok": True,
            "sale_ok": False,
            "can_be_expensed": True,
            "list_price": 175.0,
        })
        product = tmpl.product_variant_id
    else:
        product = products[0].product_variant_id

    # Create the expense (draft).
    expense = env["hr.expense"].create({
        "name": EXPENSE_NAME,
        "employee_id": emp.id,
        "product_id": product.id,
        "total_amount": 175.0,
        "quantity": 1.0,
        "date": "2026-04-08",
    })

    # Create the expense report and attach the expense. Leave in draft.
    env["hr.expense.sheet"].create({
        "name": REPORT_NAME,
        "employee_id": emp.id,
        "expense_line_ids": [(6, 0, [expense.id])],
    })

    # Make sure admin has expense manager + accountant rights.
    for grp_ref in [
        "hr_expense.group_hr_expense_team_approver",
        "hr_expense.group_hr_expense_manager",
        "hr_expense.group_hr_expense_user",
        "account.group_account_invoice",
        "account.group_account_user",
    ]:
        group = env.ref(grp_ref, raise_if_not_found=False)
        if group and group not in admin.group_ids:
            admin.write({"group_ids": [(4, group.id)]})
