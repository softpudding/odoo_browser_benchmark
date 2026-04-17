"""Seed for hr_expense.create_expense_report_submit.

Category 2 (MEDIUM): Create an expense and submit it for approval.
The agent must fill in expense details and navigate the submit workflow.
"""


def setup(env):
    # Cleanup prior runs
    prior = env["hr.expense"].search([
        ("name", "=", "Hotel stay - Berlin conference"),
    ])
    if prior:
        # Reset submitted expenses before deleting
        for exp in prior:
            if exp.state in ("approved", "submitted"):
                try:
                    exp.action_refuse()
                except Exception:
                    pass
            try:
                exp.unlink()
            except Exception:
                pass

    # Ensure admin has an employee record
    admin = env.ref("base.user_admin")
    employee = env["hr.employee"].search([("user_id", "=", admin.id)], limit=1)
    if not employee:
        env["hr.employee"].create({
            "name": admin.name,
            "user_id": admin.id,
        })

    # Ensure an expense product exists (for the Category/Product field)
    exp_product = env["product.product"].search([
        ("can_be_expensed", "=", True),
    ], limit=1)
    if not exp_product:
        env["product.template"].create({
            "name": "Travel Expenses",
            "type": "service",
            "can_be_expensed": True,
            "list_price": 0.0,
            "standard_price": 0.0,
        })
