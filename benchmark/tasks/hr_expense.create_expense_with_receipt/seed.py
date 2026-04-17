"""Seed a vendor partner, expense category, and employee for the task."""


EXPENSE_NAME = "Client dinner at Harborview"
CATEGORY_NAME = "Client Meals"
VENDOR_NAME = "Harborview Restaurant Group"


def setup(env):
    env["hr.expense"].search([("name", "=", EXPENSE_NAME)]).unlink()

    admin_employee = env["hr.employee"].search(
        [("user_id", "=", env.ref("base.user_admin").id)], limit=1
    )
    if not admin_employee:
        admin_employee = env["hr.employee"].create({
            "name": "Administrator",
            "user_id": env.ref("base.user_admin").id,
        })

    vendor = env["res.partner"].search([("name", "=", VENDOR_NAME)], limit=1)
    if not vendor:
        vendor = env["res.partner"].create({
            "name": VENDOR_NAME,
            "supplier_rank": 1,
            "is_company": True,
        })

    category = env["product.template"].search(
        [("name", "=", CATEGORY_NAME)], limit=1
    )
    if not category:
        category = env["product.template"].create({
            "name": CATEGORY_NAME,
            "type": "service",
            "purchase_ok": True,
            "sale_ok": False,
            "can_be_expensed": True,
            "list_price": 0.0,
        })
