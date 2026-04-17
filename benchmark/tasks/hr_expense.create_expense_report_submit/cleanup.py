"""Clean up artifacts from previous runs."""


def cleanup(env):
    expenses = env["hr.expense"].search([
        ("name", "=", "Hotel stay - Berlin conference"),
    ])
    for exp in expenses:
        if exp.state in ("approved", "submitted"):
            try:
                exp.action_refuse()
            except Exception:
                pass
        try:
            exp.unlink()
        except Exception:
            pass
