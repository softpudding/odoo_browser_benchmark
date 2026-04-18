"""Seed for hr_expense.create_with_currency_eur_to_usd.

Sets up:
- Activates EUR currency and creates a deterministic USD->EUR rate (1 USD = 0.925 EUR).
- Grants the admin the Multi-Currency group so the Currency dropdown is visible
  on the expense form.
- Creates a 'Hotel' expense category.
- Ensures admin has an hr.employee.

The agent must create an expense in EUR (185.00), which converts to ~$200 USD
in the company currency.
"""

EXPENSE_NAME = "NYC Hotel"
CATEGORY_NAME = "Hotel"


def _cleanup(env):
    expenses = env["hr.expense"].search([("name", "=", EXPENSE_NAME)])
    for expense in expenses:
        if expense.account_move_id and expense.account_move_id.state == "posted":
            expense.account_move_id.button_draft()
        if expense.state != "draft":
            try:
                expense.action_reset()
            except Exception:
                pass
        attachments = env["ir.attachment"].search([
            ("res_model", "=", "hr.expense"),
            ("res_id", "=", expense.id),
        ])
        attachments.unlink()
        expense.unlink()


def setup(env):
    _cleanup(env)

    # 1. Grant admin Multi-Currency group so the Currency dropdown appears on the form.
    admin = env.ref("base.user_admin")
    multi_currency_grp = env.ref("base.group_multi_currency")
    admin.group_ids |= multi_currency_grp
    # Also grant Expense manager so admin can edit any expense.
    admin.group_ids |= env.ref("hr_expense.group_hr_expense_manager")

    # 2. Activate EUR.
    eur = env.ref("base.EUR")
    if not eur.active:
        eur.sudo().write({"active": True})

    # 3. Set a deterministic exchange rate. Company currency = USD; rate field
    #    is "currency-per-company-currency", so 0.925 means 1 USD = 0.925 EUR.
    #    With this rate, 185 EUR -> 185 / 0.925 = 200.00 USD.
    company = env.company
    rate_date = "2026-01-01"
    existing = env["res.currency.rate"].search([
        ("currency_id", "=", eur.id),
        ("name", "=", rate_date),
        ("company_id", "in", (False, company.id)),
    ])
    if existing:
        existing.write({"rate": 0.925})
    else:
        env["res.currency.rate"].create({
            "name": rate_date,
            "currency_id": eur.id,
            "rate": 0.925,
            "company_id": company.id,
        })

    # 4. Ensure admin has an employee record.
    employee = admin.employee_id
    if not employee:
        employee = env["hr.employee"].create({
            "name": "Administrator",
            "work_email": "admin@example.com",
            "user_id": admin.id,
        })

    # 5. Create the Hotel expense category if not present.
    category = env["product.product"].search([
        ("name", "=", CATEGORY_NAME),
        ("can_be_expensed", "=", True),
    ], limit=1)
    if not category:
        tmpl = env["product.template"].create({
            "name": CATEGORY_NAME,
            "type": "service",
            "purchase_ok": True,
            "sale_ok": False,
            "can_be_expensed": True,
            "standard_price": 0.0,
            "list_price": 0.0,
        })
        category = tmpl.product_variant_id
