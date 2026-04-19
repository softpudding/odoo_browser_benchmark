"""Cleanup for hr_expense.scan_submit_expense_from_mobile_portal.

Removes the seeded `Travel - Taxi` product template and any `Airport taxi`
expense records (including previously-posted account moves) so re-runs start
clean.
"""


PRODUCT_NAME = "Travel - Taxi"
EXPENSE_NAME = "Airport taxi"


def cleanup(env):
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

    tmpl = env["product.template"].search([("name", "=", PRODUCT_NAME)])
    try:
        tmpl.unlink()
    except Exception:
        pass
