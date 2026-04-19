"""Seed for hr_expense.scan_submit_expense_from_mobile_portal.

Creates an expensable product category `Travel - Taxi` (service, price 25.00)
that the agent must pick when logging a taxi ride. Ensures admin has an
hr.employee record so the expense form auto-fills correctly, and cleans up any
previously-created `Airport taxi` expense so the task is idempotent.
"""


PRODUCT_NAME = "Travel - Taxi"
EXPENSE_NAME = "Airport taxi"


def _cleanup(env):
    # Remove any prior `Airport taxi` expense (including posted/approved states).
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
        try:
            exp.unlink()
        except Exception:
            pass


def setup(env):
    admin = env.ref("base.user_admin")

    # Make sure admin has the expense groups (own-expense submission needs user).
    for grp_ref in [
        "hr_expense.group_hr_expense_user",
        "hr_expense.group_hr_expense_team_approver",
        "hr_expense.group_hr_expense_manager",
    ]:
        group = env.ref(grp_ref, raise_if_not_found=False)
        if group and group not in admin.group_ids:
            admin.write({"group_ids": [(4, group.id)]})

    # Ensure admin has an hr.employee (needed so the expense form auto-fills
    # employee_id). The demo DB usually has one; create one if not.
    emp = env["hr.employee"].search([("user_id", "=", admin.id)], limit=1)
    if not emp:
        emp = env["hr.employee"].create({
            "name": admin.name or "Administrator",
            "user_id": admin.id,
            "work_email": admin.email or "admin@example.com",
        })

    _cleanup(env)

    # Create/update the expensable product category "Travel - Taxi".
    # Important: Keep standard_price=0.0 so product_has_cost=False. When
    # product_has_cost is True in Odoo 19, the total_amount_currency field
    # becomes READONLY on the form (total is computed from quantity *
    # price_unit), which would prevent the agent from typing 45.00
    # directly. With standard_price=0.0, total_amount_currency is editable.
    tmpl = env["product.template"].search([("name", "=", PRODUCT_NAME)], limit=1)
    vals = {
        "type": "service",
        "purchase_ok": True,
        "sale_ok": False,
        "can_be_expensed": True,
        "list_price": 25.00,
        "standard_price": 0.0,
    }
    if not tmpl:
        vals["name"] = PRODUCT_NAME
        tmpl = env["product.template"].create(vals)
    else:
        tmpl.write(vals)
