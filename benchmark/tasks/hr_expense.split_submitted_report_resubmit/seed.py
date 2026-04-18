"""Seed for hr_expense.split_submitted_report_resubmit.

Odoo 19 removed hr.expense.sheet; the approval workflow now runs directly on
hr.expense. This seed creates 3 submitted expenses for Lee Bench sharing the
trip identifier R-BENCH-SPLIT-001:
  - R-BENCH-SPLIT-001 Meal (Meals, 40.00)
  - R-BENCH-SPLIT-001 Gadget (Office Supplies, 500.00, non-compliant)
  - R-BENCH-SPLIT-001 Taxi  (Travel, 25.00)

Manager task: refuse the Gadget line with reason "Not compliant" and approve
the other two, effectively splitting the submitted batch.
"""

EMPLOYEE_NAME = "Lee Bench"
EMPLOYEE_EMAIL = "lee.bench@example.com"

MEAL_NAME = "R-BENCH-SPLIT-001 Meal"
GADGET_NAME = "R-BENCH-SPLIT-001 Gadget"
TAXI_NAME = "R-BENCH-SPLIT-001 Taxi"

MEAL_PRODUCT = "Bench Meals"
GADGET_PRODUCT = "Bench Office Supplies"
TAXI_PRODUCT = "Bench Travel"

EXPENSE_NAMES = [MEAL_NAME, GADGET_NAME, TAXI_NAME]


def _ensure_product(env, name, list_price):
    product = env["product.product"].search(
        [("name", "=", name), ("can_be_expensed", "=", True)],
        limit=1,
    )
    if product:
        return product
    tmpl = env["product.template"].create({
        "name": name,
        "type": "service",
        "purchase_ok": True,
        "sale_ok": False,
        "can_be_expensed": True,
        "list_price": list_price,
        "standard_price": list_price,
    })
    return tmpl.product_variant_id


def _cleanup(env):
    expenses = env["hr.expense"].with_context(active_test=False).search([
        ("name", "in", EXPENSE_NAMES),
    ])
    for exp in expenses:
        # If any was split, any child expenses are also cleaned up
        children = env["hr.expense"].with_context(active_test=False).search([
            ("split_expense_origin_id", "=", exp.id),
        ])
        for child in children:
            try:
                if child.state != "draft":
                    child.action_reset()
            except Exception:
                pass
            try:
                if child.account_move_id:
                    if child.account_move_id.state == "posted":
                        child.account_move_id.button_draft()
                    child.account_move_id.unlink()
            except Exception:
                pass
            child.unlink()
        try:
            if exp.state != "draft":
                exp.action_reset()
        except Exception:
            pass
        try:
            if exp.account_move_id:
                if exp.account_move_id.state == "posted":
                    exp.account_move_id.button_draft()
                exp.account_move_id.unlink()
        except Exception:
            pass
        attachments = env["ir.attachment"].search([
            ("res_model", "=", "hr.expense"),
            ("res_id", "=", exp.id),
        ])
        attachments.unlink()
        exp.unlink()


def setup(env):
    admin = env.ref("base.user_admin")

    # Ensure admin has the expense-approver groups (manager can approve/refuse).
    for grp_ref in [
        "hr_expense.group_hr_expense_team_approver",
        "hr_expense.group_hr_expense_manager",
        "hr_expense.group_hr_expense_user",
    ]:
        group = env.ref(grp_ref, raise_if_not_found=False)
        if group and group not in admin.group_ids:
            admin.write({"group_ids": [(4, group.id)]})

    _cleanup(env)

    # Create/update the employee with admin as expense manager so admin can approve.
    emp = env["hr.employee"].search([("name", "=", EMPLOYEE_NAME)], limit=1)
    if not emp:
        emp = env["hr.employee"].create({
            "name": EMPLOYEE_NAME,
            "work_email": EMPLOYEE_EMAIL,
            "expense_manager_id": admin.id,
        })
    else:
        emp.write({"expense_manager_id": admin.id, "work_email": EMPLOYEE_EMAIL})

    meal_product = _ensure_product(env, MEAL_PRODUCT, 40.0)
    gadget_product = _ensure_product(env, GADGET_PRODUCT, 500.0)
    taxi_product = _ensure_product(env, TAXI_PRODUCT, 25.0)

    def _mk(name, product, amount):
        return env["hr.expense"].create({
            "name": name,
            "employee_id": emp.id,
            "product_id": product.id,
            "total_amount_currency": amount,
            "quantity": 1.0,
            "date": "2026-04-10",
            "payment_mode": "own_account",
        })

    expenses = env["hr.expense"]
    expenses |= _mk(MEAL_NAME, meal_product, 40.0)
    expenses |= _mk(GADGET_NAME, gadget_product, 500.0)
    expenses |= _mk(TAXI_NAME, taxi_product, 25.0)

    # Submit them so they land in the approver queue.
    for exp in expenses:
        try:
            exp.action_submit()
        except Exception:
            # fall back: write approval_state directly
            exp.sudo().write({"approval_state": "submitted"})
