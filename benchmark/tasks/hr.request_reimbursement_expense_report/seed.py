"""Seed for hr.request_reimbursement_expense_report.

Category 1: closed-loop cross-module (expenses → accounting).

Creates a draft `Bench Travel Expense` (total 150.00, own_account, expensable
service product) owned by admin's `hr.employee`. The agent must walk the full
Odoo 19 reimbursement lifecycle: Submit → Approve → Post Journal Entries. The
Post Journal Entries step triggers a modal wizard whose primary button must
be clicked to create & post the accounting entry, landing the hr.expense in
the `posted` state (the v19 equivalent of the old `hr.expense.sheet.state='done'`).

Key design choices:
  * `hr.expense.sheet` is removed in Odoo 19; approval runs directly on
    hr.expense. Cannot seed a sheet.
  * A dedicated `Bench Expense Manager` user is created and set as
    admin.employee_id.expense_manager_id so that `_can_be_autovalidated`
    returns False on submit — otherwise admin submitting their own
    expense would auto-jump straight to `approved`, turning the 3-step
    workflow into 1 step and defeating the task design.
  * Admin is granted all three hr_expense groups + account.group_account_invoice
    so Approve and Post Journal Entries are both visible from the statusbar.
  * The expensable product uses `standard_price=0.0` to keep the Total
    field editable (for idempotency across reruns; the agent does not
    edit Total in this task but we keep the expense editable for
    cleanup).
"""


EXPENSE_NAME = "Bench Travel Expense"
PRODUCT_NAME = "Bench Travel Service"
MANAGER_LOGIN = "bench_expense_manager"
MANAGER_NAME = "Bench Expense Manager"
MANAGER_EMAIL = "bench.expense.manager@example.com"


def _cleanup(env):
    """Remove any prior expense and account.move from a previous run."""
    expenses = env["hr.expense"].with_context(active_test=False).search([
        ("name", "=", EXPENSE_NAME),
    ])
    for exp in expenses:
        try:
            if exp.state not in ("draft",):
                exp.action_reset()
        except Exception:
            pass
        try:
            if exp.account_move_id:
                move = exp.account_move_id
                if move.state == "posted":
                    try:
                        move.button_draft()
                    except Exception:
                        pass
                try:
                    move.unlink()
                except Exception:
                    pass
        except Exception:
            pass
        attachments = env["ir.attachment"].search([
            ("res_model", "=", "hr.expense"),
            ("res_id", "=", exp.id),
        ])
        attachments.unlink()
        try:
            exp.unlink()
        except Exception:
            pass


def _ensure_manager_user(env):
    user = env["res.users"].with_context(active_test=False).search(
        [("login", "=", MANAGER_LOGIN)], limit=1,
    )
    if not user:
        user = env["res.users"].create({
            "name": MANAGER_NAME,
            "login": MANAGER_LOGIN,
            "email": MANAGER_EMAIL,
        })
    if not user.active:
        user.active = True

    emp = env["hr.employee"].search([("user_id", "=", user.id)], limit=1)
    if not emp:
        env["hr.employee"].create({
            "name": MANAGER_NAME,
            "user_id": user.id,
            "work_email": MANAGER_EMAIL,
        })
    return user


def _ensure_product(env):
    product = env["product.product"].search(
        [("name", "=", PRODUCT_NAME), ("can_be_expensed", "=", True)],
        limit=1,
    )
    if product:
        return product
    tmpl = env["product.template"].create({
        "name": PRODUCT_NAME,
        "type": "service",
        "purchase_ok": True,
        "sale_ok": False,
        "can_be_expensed": True,
        "list_price": 150.00,
        "standard_price": 0.0,
    })
    return tmpl.product_variant_id


def setup(env):
    admin = env.ref("base.user_admin")

    # Grant admin the three hr_expense groups + the accounting invoice group so
    # Submit / Approve / Post Journal Entries are all visible on the statusbar.
    for grp_ref in [
        "hr_expense.group_hr_expense_user",
        "hr_expense.group_hr_expense_team_approver",
        "hr_expense.group_hr_expense_manager",
        "account.group_account_invoice",
    ]:
        group = env.ref(grp_ref, raise_if_not_found=False)
        if group and group not in admin.group_ids:
            admin.write({"group_ids": [(4, group.id)]})

    # Make sure admin has an hr.employee (the expense is owned by it).
    admin_emp = env["hr.employee"].search([("user_id", "=", admin.id)], limit=1)
    if not admin_emp:
        admin_emp = env["hr.employee"].create({
            "name": admin.name or "Administrator",
            "user_id": admin.id,
            "work_email": admin.email or "admin@example.com",
        })

    # A *different* user must be admin's expense_manager — otherwise
    # `_can_be_autovalidated` returns True on submit (manager_id equals the
    # employee's user) and the expense jumps straight from Draft to Approved,
    # collapsing the 3-step workflow this task is built around.
    manager_user = _ensure_manager_user(env)
    admin_emp.write({"expense_manager_id": manager_user.id})

    _cleanup(env)

    product = _ensure_product(env)

    expense = env["hr.expense"].create({
        "name": EXPENSE_NAME,
        "employee_id": admin_emp.id,
        "product_id": product.id,
        "total_amount_currency": 150.00,
        "quantity": 1.0,
        "date": "2026-04-15",
        "payment_mode": "own_account",
        # Explicitly set manager_id too so action_submit does not overwrite it
        # with the default_responsible_for_approval (both resolve to manager_user
        # but being explicit is clearer on read).
        "manager_id": manager_user.id,
    })

    # Sanity: make sure it really is draft (belt & suspenders for reruns).
    if expense.state != "draft":
        try:
            expense.action_reset()
        except Exception:
            pass
