"""Seed for hr_expense.reject_expense_report_with_feedback.

Category: recovery_rollback (MEDIUM).

Creates an expense report 'SUMMIT-2026' in 'submit' state for employee
'Alice Benchmark', with one hotel expense line. The task is to refuse
(reject) this report with a written reason.
"""

EMPLOYEE_NAME = "Alice Benchmark"
PRODUCT_NAME = "Benchmark Hotel Over-cap"
EXPENSE_NAME = "Overpriced hotel night"
REPORT_NAME = "SUMMIT-2026 – Summit trip reimbursement"


def setup(env):
    admin = env.ref("base.user_admin")

    # Cleanup prior runs.
    prior_reports = env["hr.expense.sheet"].search([
        ("name", "=", REPORT_NAME),
    ])
    for sheet in prior_reports:
        if sheet.state in ("approve",):
            try:
                sheet.action_refuse_expense_sheets()
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

    # Create the expense line.
    expense = env["hr.expense"].create({
        "name": EXPENSE_NAME,
        "employee_id": emp.id,
        "product_id": product.id,
        "total_amount": 320.0,
        "quantity": 1.0,
        "date": "2026-05-02",
    })

    # Create the expense report (sheet) and attach the expense.
    sheet = env["hr.expense.sheet"].create({
        "name": REPORT_NAME,
        "employee_id": emp.id,
        "expense_line_ids": [(6, 0, [expense.id])],
    })

    # Submit the sheet so it lands in the approver's To Approve list.
    try:
        sheet.action_submit_sheet()
    except Exception:
        # Fallback: some Odoo versions use a different method name.
        try:
            sheet.action_submit_expense_sheets()
        except Exception:
            pass

    # Make sure admin has expense manager rights to refuse.
    for grp_ref in [
        "hr_expense.group_hr_expense_team_approver",
        "hr_expense.group_hr_expense_manager",
        "hr_expense.group_hr_expense_user",
    ]:
        group = env.ref(grp_ref, raise_if_not_found=False)
        if group and group not in admin.group_ids:
            admin.write({"group_ids": [(4, group.id)]})
