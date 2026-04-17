"""Postcondition checks for hr_expense.create_expense_with_receipt."""

from datetime import date

REQUIRED_NOTE = "Q2 client retention dinner - VIP attendee list on file"


def check(env):
    failures = []

    exps = env["hr.expense"].search([
        ("name", "=", "Client dinner at Harborview"),
    ])
    if not exps:
        return ["No expense found with description 'Client dinner at Harborview'"]
    if len(exps) > 1:
        failures.append(f"Found {len(exps)} expenses, expected exactly 1")

    exp = exps[0]

    if exp.state != "draft":
        failures.append(f"State is '{exp.state}', expected 'draft'")

    if exp.payment_mode != "company_account":
        failures.append(
            f"payment_mode is '{exp.payment_mode}', expected 'company_account' (Paid By: Company)"
        )

    if exp.product_id.name != "Client Meals":
        failures.append(
            f"Category is '{exp.product_id.name}', expected 'Client Meals'"
        )

    if exp.vendor_id.name != "Harborview Restaurant Group":
        failures.append(
            f"Vendor is '{exp.vendor_id.name}', expected 'Harborview Restaurant Group'"
        )

    if abs(exp.total_amount - 185.50) > 0.01:
        failures.append(
            f"Total is {exp.total_amount}, expected 185.50"
        )

    exp_date = exp.date
    if exp_date != date(2026, 5, 12):
        failures.append(f"Expense date is {exp_date}, expected 2026-05-12")

    description = (exp.description or "").strip()
    if REQUIRED_NOTE not in description:
        failures.append(
            f"Internal Notes missing expected text; got: {description!r}"
        )

    return failures
