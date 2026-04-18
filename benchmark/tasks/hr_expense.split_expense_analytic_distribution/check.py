"""Postcondition checks for hr_expense.split_expense_analytic_distribution.

Verifies:
1. Exactly one expense named 'Bench Split Travel' exists.
2. Its analytic_distribution references exactly the two expected
   analytic accounts (Bench Project Alpha + Bench Project Beta) and
   the percentages sum to 100.0.
3. The expense has been submitted (state == 'submitted' or
   approval_state == 'submitted').
4. Amount, employee, and product were not modified.
"""

EXPENSE_NAME = "Bench Split Travel"
EMPLOYEE_NAME = "Morgan Pearce"
PRODUCT_NAME = "Benchmark Travel Split"
ALPHA_NAME = "Bench Project Alpha"
BETA_NAME = "Bench Project Beta"


def _expand_keys(distribution):
    """Yield every analytic account id referenced by the distribution.

    analytic_distribution is stored as {"<id>": percent} or
    {"<id1>,<id2>": percent} for cross-plan composite keys. Return the
    flat list of referenced ids (as ints) paired with percentages
    distributed per key (percent is the weight for the whole key).
    """
    out = []
    for key, percent in (distribution or {}).items():
        ids = []
        for part in str(key).split(","):
            part = part.strip()
            if part.isdigit():
                ids.append(int(part))
        out.append((ids, float(percent)))
    return out


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

    # State transitioned from draft to submitted.
    state_ok = exp.state == "submitted" or getattr(
        exp, "approval_state", None
    ) == "submitted"
    if not state_ok:
        failures.append(
            f"Expense state is '{exp.state}' "
            f"(approval_state="
            f"{getattr(exp, 'approval_state', None)!r}), "
            f"expected 'submitted'"
        )

    # Amount, employee, product unchanged.
    if abs(exp.total_amount_currency - 200.00) > 0.01:
        failures.append(
            f"Expense total is {exp.total_amount_currency}, "
            f"expected 200.00 (amount must not be modified)"
        )
    if (exp.employee_id.name or "") != EMPLOYEE_NAME:
        failures.append(
            f"Expense employee is '{exp.employee_id.name}', "
            f"expected '{EMPLOYEE_NAME}'"
        )
    if (exp.product_id.name or "") != PRODUCT_NAME:
        failures.append(
            f"Expense product is '{exp.product_id.name}', "
            f"expected '{PRODUCT_NAME}'"
        )

    # Analytic distribution checks.
    distribution = exp.analytic_distribution or {}
    if not distribution:
        failures.append(
            "Expense analytic_distribution is empty — "
            "expected a 50/50 split across two analytic accounts"
        )
        return failures

    # Expected analytic account records.
    alpha = env["account.analytic.account"].search(
        [("name", "=", ALPHA_NAME)], limit=1
    )
    beta = env["account.analytic.account"].search(
        [("name", "=", BETA_NAME)], limit=1
    )
    if not alpha:
        failures.append(
            f"Analytic account '{ALPHA_NAME}' not found in DB"
        )
    if not beta:
        failures.append(
            f"Analytic account '{BETA_NAME}' not found in DB"
        )
    if not (alpha and beta):
        return failures

    entries = _expand_keys(distribution)

    # Total percentage should sum to 100.
    total_pct = sum(pct for _ids, pct in entries)
    if abs(total_pct - 100.0) > 0.01:
        failures.append(
            f"Analytic distribution percentages sum to {total_pct}, "
            f"expected 100.0 (distribution={distribution!r})"
        )

    # Flatten referenced analytic ids.
    referenced_ids = set()
    for ids, _pct in entries:
        referenced_ids.update(ids)

    expected_ids = {alpha.id, beta.id}
    extra = referenced_ids - expected_ids
    missing = expected_ids - referenced_ids
    if extra:
        extra_names = [
            a.display_name
            for a in env["account.analytic.account"].browse(list(extra))
        ]
        failures.append(
            f"Analytic distribution references unexpected account(s): "
            f"{extra_names} (distribution={distribution!r})"
        )
    if missing:
        miss_names = [
            a.display_name
            for a in env["account.analytic.account"].browse(list(missing))
        ]
        failures.append(
            f"Analytic distribution is missing expected account(s): "
            f"{miss_names} (distribution={distribution!r})"
        )

    # Each expected account must account for 50.0% of the total.
    alpha_pct = 0.0
    beta_pct = 0.0
    for ids, pct in entries:
        if alpha.id in ids:
            alpha_pct += pct
        if beta.id in ids:
            beta_pct += pct
    if abs(alpha_pct - 50.0) > 0.01:
        failures.append(
            f"'{ALPHA_NAME}' has {alpha_pct}% in distribution, "
            f"expected 50.0% (distribution={distribution!r})"
        )
    if abs(beta_pct - 50.0) > 0.01:
        failures.append(
            f"'{BETA_NAME}' has {beta_pct}% in distribution, "
            f"expected 50.0% (distribution={distribution!r})"
        )

    return failures
