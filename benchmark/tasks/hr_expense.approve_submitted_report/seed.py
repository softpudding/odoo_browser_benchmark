"""Seed for hr_expense.approve_submitted_report.

Category: policy_trap (MEDIUM).
Pre-creates two submitted expenses under different employees. The agent
must approve only the Alpha one and leave the Beta distractor
untouched.

Odoo 19 unified hr.expense.sheet into hr.expense — each expense has its
own state ('draft' → 'submitted' → 'approved').
"""

TARGET_EXPENSE = "Alpha project travel 2026"
DISTRACTOR_EXPENSE = "Beta client lunch 2026"
TARGET_EMP = "Priya Mehta"
DISTRACTOR_EMP = "Ethan Brooks"


def setup(env):
    Expense = env["hr.expense"]
    Employee = env["hr.employee"]
    Product = env["product.product"]

    # Cleanup prior runs.
    stale = Expense.search([
        ("name", "in", [TARGET_EXPENSE, DISTRACTOR_EXPENSE]),
    ])
    for e in stale:
        if e.state != "draft":
            try:
                e.action_reset()
            except Exception:
                pass
    stale.unlink()

    admin = env.ref("base.user_admin")
    admin.group_ids |= env.ref("hr_expense.group_hr_expense_manager")

    product = Product.search(
        [("can_be_expensed", "=", True)], limit=1
    )
    if not product:
        tmpl = env["product.template"].create({
            "name": "[GEN] General Expense",
            "type": "service",
            "can_be_expensed": True,
            "standard_price": 0.0,
            "list_price": 0.0,
        })
        product = tmpl.product_variant_id

    def _ensure_employee(name):
        emp = Employee.search([("name", "=", name)], limit=1)
        if not emp:
            emp = Employee.create({
                "name": name,
                "work_email": (
                    name.lower().replace(" ", ".") + "@example.com"
                ),
            })
        emp.expense_manager_id = admin
        return emp

    target_emp = _ensure_employee(TARGET_EMP)
    distractor_emp = _ensure_employee(DISTRACTOR_EMP)

    def _create_submitted(name, employee, total):
        expense = Expense.create({
            "name": name,
            "employee_id": employee.id,
            "product_id": product.id,
            "total_amount_currency": total,
            "quantity": 1,
            "date": "2026-04-10",
        })
        expense.action_submit()
        return expense

    _create_submitted(TARGET_EXPENSE, target_emp, 450.0)
    _create_submitted(DISTRACTOR_EXPENSE, distractor_emp, 220.0)
