"""Postcondition checks for hr_expense.submit_approve_post_accounting."""


EXPENSE_NAME = "TRV-2026-04 — April client visit"


def check(env):
    failures = []

    expenses = env["hr.expense"].search([("name", "=", EXPENSE_NAME)])
    if not expenses:
        return [f"No expense found named '{EXPENSE_NAME}'"]
    if len(expenses) > 1:
        failures.append(f"Found {len(expenses)} expenses, expected 1")
    exp = expenses[0]

    if exp.state not in ("posted", "in_payment", "paid"):
        failures.append(
            f"Expense state is '{exp.state}', expected 'posted' (or later)"
        )

    move = getattr(exp, "account_move_id", None)
    if not move:
        failures.append(
            "No account.move linked to the expense — the expense must be "
            "posted to accounting"
        )
    elif move.state != "posted":
        failures.append(
            f"Linked account.move state is '{move.state}', expected 'posted'"
        )

    return failures
