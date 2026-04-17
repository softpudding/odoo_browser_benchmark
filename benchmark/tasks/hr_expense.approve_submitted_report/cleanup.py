"""Clean up artifacts from previous runs of hr_expense.approve_submitted_report."""


def cleanup(env):
    Expense = env["hr.expense"]

    stale = Expense.search([
        ("name", "in", [
            "Alpha project travel 2026",
            "Beta client lunch 2026",
        ]),
    ])
    for e in stale:
        if e.state != "draft":
            try:
                e.action_reset()
            except Exception:
                pass
    stale.unlink()
