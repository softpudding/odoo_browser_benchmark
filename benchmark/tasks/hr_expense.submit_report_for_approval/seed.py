"""Seed for hr_expense.submit_report_for_approval.

The admin needs an associated hr.employee and expense manager so the
Submit to Manager button is available. Uses the built-in
'Travel & Accommodation' demo product as the expense category.
Cleans up any prior 'Hotel in Paris' expenses from previous runs.
"""

EXPENSE_NAME = "Hotel in Paris"
PRODUCT_NAME = "Travel & Accommodation"


def _cleanup(env):
    prior = env["hr.expense"].search([("name", "=", EXPENSE_NAME)])
    for expense in prior:
        move = getattr(expense, "account_move_id", None)
        if move and move.state == "posted":
            try:
                move.button_draft()
            except Exception:
                pass
        if move:
            try:
                move.unlink()
            except Exception:
                pass
        if expense.state != "draft":
            try:
                expense.action_reset()
            except Exception:
                pass
    prior.unlink()


def setup(env):
    _cleanup(env)

    admin = env.ref("base.user_admin")

    # Ensure admin has an associated hr.employee record.
    employee = admin.employee_id
    if not employee:
        employee = env["hr.employee"].search(
            [("user_id", "=", admin.id)], limit=1
        )
    if not employee:
        employee = env["hr.employee"].create({
            "name": admin.name or "Administrator",
            "user_id": admin.id,
            "work_email": admin.email or "admin@example.com",
        })

    # Make the admin their own expense manager so the Submit button works.
    employee.write({"expense_manager_id": admin.id})

    # Make sure admin has expense approver/manager rights so the flow
    # works end-to-end (the task only requires Submit, but having rights
    # keeps the workflow unblocked).
    for grp_ref in [
        "hr_expense.group_hr_expense_user",
        "hr_expense.group_hr_expense_team_approver",
        "hr_expense.group_hr_expense_manager",
    ]:
        group = env.ref(grp_ref, raise_if_not_found=False)
        if group and group not in admin.group_ids:
            admin.write({"group_ids": [(4, group.id)]})

    # Verify the Travel & Accommodation demo product exists and is
    # available for expenses.
    product = env["product.product"].search(
        [("name", "=", PRODUCT_NAME), ("can_be_expensed", "=", True)],
        limit=1,
    )
    if not product:
        # Fallback: ensure any existing product.template with this name is
        # expensable, otherwise create it.
        tmpl = env["product.template"].search(
            [("name", "=", PRODUCT_NAME)], limit=1
        )
        if tmpl:
            tmpl.write({
                "can_be_expensed": True,
                "purchase_ok": True,
                "sale_ok": False,
                "type": "service",
            })
        else:
            env["product.template"].create({
                "name": PRODUCT_NAME,
                "type": "service",
                "can_be_expensed": True,
                "purchase_ok": True,
                "sale_ok": False,
                "list_price": 0.0,
                "standard_price": 0.0,
            })
