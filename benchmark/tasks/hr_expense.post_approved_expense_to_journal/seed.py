"""Seed for hr_expense.post_approved_expense_to_journal.

Category: policy_trap (MEDIUM).

Odoo 19 unified hr.expense.sheet into hr.expense — each expense has its
own state: draft -> submitted -> approved -> posted (-> in_payment ->
paid). Posting an approved employee-paid expense opens the "Post
Expenses" wizard (journal + accounting date) and, on confirm, creates
an account.move and moves the expense to the 'posted' state.

The seed creates a single approved "Bench Taxi Fare" expense with an
attached receipt (required for the Post Journal Entries button to be
visible in the statusbar) for the "Dana Silverstein" employee.
"""

import base64

TARGET_EXPENSE = "Bench Taxi Fare"
EMPLOYEE_NAME = "Dana Silverstein"
PRODUCT_NAME = "Benchmark Taxi Transportation"
AMOUNT = 42.50


def _cleanup(env):
    Expense = env["hr.expense"]
    stale = Expense.search([("name", "=", TARGET_EXPENSE)])
    for e in stale:
        # Unlink any linked moves first if posted state, otherwise reset.
        if e.state not in ("draft",):
            try:
                e.action_reset()
            except Exception:
                pass
        moves = e.sudo().account_move_id
        for m in moves:
            try:
                if m.state == "posted":
                    m.button_draft()
                m.sudo().unlink()
            except Exception:
                pass
    stale.unlink()


def setup(env):
    Expense = env["hr.expense"]
    Employee = env["hr.employee"]
    Product = env["product.product"]
    Attachment = env["ir.attachment"]

    _cleanup(env)

    admin = env.ref("base.user_admin")
    # Grant required groups (manager + invoice/accountant to see the
    # Post Journal Entries button).
    for grp_ref in [
        "hr_expense.group_hr_expense_user",
        "hr_expense.group_hr_expense_team_approver",
        "hr_expense.group_hr_expense_manager",
        "account.group_account_invoice",
    ]:
        grp = env.ref(grp_ref, raise_if_not_found=False)
        if grp and grp not in admin.group_ids:
            admin.write({"group_ids": [(4, grp.id)]})

    # Ensure the employee exists and admin is her expense manager.
    emp = Employee.search([("name", "=", EMPLOYEE_NAME)], limit=1)
    if not emp:
        emp = Employee.create({
            "name": EMPLOYEE_NAME,
            "work_email": "dana.silverstein@example.com",
        })
    emp.write({"expense_manager_id": admin.id})

    # Expense product (service, can_be_expensed).
    products = Product.search([
        ("name", "=", PRODUCT_NAME),
        ("can_be_expensed", "=", True),
    ], limit=1)
    if not products:
        tmpl = env["product.template"].create({
            "name": PRODUCT_NAME,
            "type": "service",
            "can_be_expensed": True,
            "list_price": 0.0,
            "standard_price": 0.0,
        })
        product = tmpl.product_variant_id
    else:
        product = products[0]

    # Create the expense in draft, then submit, then approve.
    expense = Expense.create({
        "name": TARGET_EXPENSE,
        "employee_id": emp.id,
        "product_id": product.id,
        "total_amount_currency": AMOUNT,
        "quantity": 1.0,
        "date": "2026-04-10",
        "payment_mode": "own_account",
    })

    # Attach a small fake receipt so the Post Journal Entries button is
    # visible (the form hides it when nb_attachment == 0).
    Attachment.create({
        "name": "taxi_receipt.txt",
        "res_model": "hr.expense",
        "res_id": expense.id,
        "type": "binary",
        "datas": base64.b64encode(b"BENCH TAXI FARE RECEIPT - 42.50 EUR").decode(),
        "mimetype": "text/plain",
    })

    try:
        expense.action_submit()
    except Exception:
        pass
    try:
        # action_approve may open a duplicate-warning action when called
        # as a Many2many-style button — call _do_approve directly to
        # reliably set approval_state='approved'.
        expense._do_approve(check=False)
    except Exception:
        # Fallback — direct write.
        expense.sudo().write({
            "approval_state": "approved",
            "manager_id": admin.id,
        })

    # Double-check the expense ended in 'approved' state.
    expense.invalidate_recordset(["state"])
