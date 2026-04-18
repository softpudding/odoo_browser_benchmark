"""Postcondition checks for hr_expense.post_approved_expense_to_journal."""


EXPENSE_NAME = "Bench Taxi Fare"


def check(env):
    failures = []

    expenses = env["hr.expense"].search([("name", "=", EXPENSE_NAME)])
    if not expenses:
        return [f"No expense found named '{EXPENSE_NAME}'"]
    if len(expenses) > 1:
        failures.append(
            f"Found {len(expenses)} expenses named '{EXPENSE_NAME}', "
            f"expected exactly 1"
        )
    exp = expenses[0]

    if exp.state != "posted":
        failures.append(
            f"Expense state is '{exp.state}', expected 'posted'"
        )

    if not exp.account_move_id:
        failures.append(
            "Expense has no linked account.move (account_move_id is False)"
        )
    else:
        move = exp.account_move_id
        if move.state not in ("posted", "draft"):
            failures.append(
                f"Linked account.move state is '{move.state}', "
                f"expected 'posted' or 'draft'"
            )
        # Guard against duplicate posted moves for the same expense.
        dup_moves = env["account.move"].search([
            ("expense_ids", "in", exp.id),
        ])
        if len(dup_moves) > 1:
            failures.append(
                f"Expected 1 account.move linked to the expense, "
                f"found {len(dup_moves)}"
            )

    if abs(exp.total_amount_currency - 42.50) > 0.01:
        failures.append(
            f"Expense total is {exp.total_amount_currency}, "
            f"expected 42.50 (amount must not be modified)"
        )

    return failures
