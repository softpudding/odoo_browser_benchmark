"""Postconditions for hr_expense.approve_submitted_report."""


def check(env):
    failures = []

    Expense = env["hr.expense"]

    target = Expense.search(
        [("name", "=", "Alpha project travel 2026")], limit=1
    )
    distractor = Expense.search(
        [("name", "=", "Beta client lunch 2026")], limit=1
    )

    if not target:
        return ["Expense 'Alpha project travel 2026' not found"]
    if not distractor:
        failures.append(
            "Expense 'Beta client lunch 2026' not found — seed may not have run"
        )

    if target.state != "approved":
        failures.append(
            f"Target expense state is '{target.state}', expected 'approved'"
        )

    if distractor and distractor.state != "submitted":
        failures.append(
            f"Distractor expense 'Beta client lunch 2026' state is "
            f"'{distractor.state}', expected 'submitted' (must not be touched)"
        )

    return failures
