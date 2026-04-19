"""Cleanup for hr.request_reimbursement_expense_report.

Reverses the seed: resets/unlinks the Bench Travel Expense, its posted
account.move, and the seeded expense manager user + product. Must handle all
possible states (draft, submitted, approved, posted, refused) because a
prior failed run may have left the expense in any of them.
"""


EXPENSE_NAME = "Bench Travel Expense"
PRODUCT_NAME = "Bench Travel Service"
MANAGER_LOGIN = "bench_expense_manager"


def cleanup(env):
    # 1) Expenses
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

    # 2) Product
    tmpl = env["product.template"].search([("name", "=", PRODUCT_NAME)])
    try:
        tmpl.unlink()
    except Exception:
        pass

    # 3) Manager user + employee. Clear admin.employee_id.expense_manager_id
    # first so we don't violate the relation on unlink.
    admin = env.ref("base.user_admin")
    admin_emp = env["hr.employee"].search([("user_id", "=", admin.id)], limit=1)
    if admin_emp and admin_emp.expense_manager_id and admin_emp.expense_manager_id.login == MANAGER_LOGIN:
        admin_emp.write({"expense_manager_id": False})

    manager_user = env["res.users"].with_context(active_test=False).search(
        [("login", "=", MANAGER_LOGIN)], limit=1,
    )
    if manager_user:
        manager_emp = env["hr.employee"].search(
            [("user_id", "=", manager_user.id)], limit=1,
        )
        try:
            if manager_emp:
                manager_emp.unlink()
        except Exception:
            pass
        try:
            manager_user.unlink()
        except Exception:
            # Fallback to archive if unlink is blocked (e.g. references).
            try:
                manager_user.active = False
            except Exception:
                pass
