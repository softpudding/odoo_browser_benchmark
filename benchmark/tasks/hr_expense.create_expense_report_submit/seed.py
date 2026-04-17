"""Seed employee and expensable product data for an expense submission task."""


EMPLOYEE_NAME = "Benchmark Expense Admin"
PRODUCT_NAME = "Hotel Stay"
EXPENSE_NAME = "Summit hotel stay"


def setup(env):
    env["hr.expense"].search([("name", "=", EXPENSE_NAME)]).unlink()

    employee = env["hr.employee"].search([("name", "=", EMPLOYEE_NAME)])
    employee.unlink()

    products = env["product.template"].search([("name", "=", PRODUCT_NAME)])
    products.unlink()

    env["hr.employee"].create({
        "name": EMPLOYEE_NAME,
        "user_id": env.user.id,
        "work_email": "benchmark.expense.admin@example.com",
    })

    env["product.template"].create({
        "name": PRODUCT_NAME,
        "type": "service",
        "purchase_ok": True,
        "sale_ok": False,
        "can_be_expensed": True,
        "list_price": 245.0,
    })
