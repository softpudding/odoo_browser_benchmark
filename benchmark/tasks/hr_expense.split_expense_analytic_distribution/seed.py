"""Seed for hr_expense.split_expense_analytic_distribution.

Category 5 (HARD): Deep UI interaction.

Force the agent to open the Analytic Distribution editor on a draft
hr.expense and split the cost evenly (50/50) across two specific
analytic accounts, then submit the expense.

The seed creates:
    * An analytic plan "Bench Plan".
    * Two analytic accounts "Bench Project Alpha" and
      "Bench Project Beta" under that plan.
    * An expense product "Benchmark Travel Split".
    * An employee "Morgan Pearce" with admin as expense manager.
    * A draft hr.expense "Bench Split Travel" for Morgan Pearce,
      200.00 EUR, state=draft.

The admin user is granted the analytic accounting group so the
Analytic Distribution field is visible, plus the standard hr_expense
groups.
"""

EXPENSE_NAME = "Bench Split Travel"
EMPLOYEE_NAME = "Morgan Pearce"
PRODUCT_NAME = "Benchmark Travel Split"
PLAN_NAME = "Bench Plan"
ALPHA_NAME = "Bench Project Alpha"
BETA_NAME = "Bench Project Beta"
AMOUNT = 200.00


def _cleanup(env):
    Expense = env["hr.expense"]
    stale = Expense.search([("name", "=", EXPENSE_NAME)])
    for e in stale:
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


def _ensure_plan(env):
    Plan = env["account.analytic.plan"]
    plan = Plan.search([("name", "=", PLAN_NAME)], limit=1)
    if not plan:
        plan = Plan.create({
            "name": PLAN_NAME,
        })
    return plan


def _ensure_analytic_account(env, name, plan):
    Account = env["account.analytic.account"]
    acc = Account.search([
        ("name", "=", name),
        ("plan_id", "=", plan.id),
    ], limit=1)
    if not acc:
        acc = Account.create({
            "name": name,
            "plan_id": plan.id,
        })
    return acc


def setup(env):
    _cleanup(env)

    admin = env.ref("base.user_admin")

    # Grant required groups: hr_expense + analytic accounting so the
    # Analytic Distribution field is visible on the expense form.
    for grp_ref in (
        "hr_expense.group_hr_expense_user",
        "hr_expense.group_hr_expense_team_approver",
        "hr_expense.group_hr_expense_manager",
        "analytic.group_analytic_accounting",
        "account.group_account_invoice",
    ):
        grp = env.ref(grp_ref, raise_if_not_found=False)
        if grp and grp not in admin.group_ids:
            admin.write({"group_ids": [(4, grp.id)]})

    # Analytic plan + two projects under it.
    plan = _ensure_plan(env)
    alpha = _ensure_analytic_account(env, ALPHA_NAME, plan)
    beta = _ensure_analytic_account(env, BETA_NAME, plan)

    # Employee with admin as expense manager so admin can submit.
    # Do NOT set employee.user_id to admin — there is a DB-level unique
    # (user_id, company_id) constraint on hr.employee and admin is
    # already linked to another employee in the base snapshot. We rely
    # on admin's hr_expense.group_hr_expense_manager rights to see and
    # submit the expense from All Expenses.
    Employee = env["hr.employee"]
    emp = Employee.search([("name", "=", EMPLOYEE_NAME)], limit=1)
    if not emp:
        emp = Employee.create({
            "name": EMPLOYEE_NAME,
            "work_email": "morgan.pearce@example.com",
            "expense_manager_id": admin.id,
        })
    else:
        emp.write({"expense_manager_id": admin.id})

    # Expense product (service, can_be_expensed).
    Product = env["product.product"]
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

    # Create the expense in draft (default state for hr.expense.create).
    expense = env["hr.expense"].create({
        "name": EXPENSE_NAME,
        "employee_id": emp.id,
        "product_id": product.id,
        "total_amount_currency": AMOUNT,
        "quantity": 1.0,
        "date": "2026-04-10",
        "payment_mode": "own_account",
    })

    # Ensure starting state is draft so the task verifies a transition.
    if expense.state != "draft":
        try:
            expense.action_reset()
        except Exception:
            pass

    # Stash analytic account ids on a context-less invalidate so the
    # read view picks them up on the form.
    expense.invalidate_recordset()

    # Record the analytic ids we care about — useful for downstream
    # debugging; also ensures both accounts are flushed to DB.
    _ = alpha.id, beta.id
