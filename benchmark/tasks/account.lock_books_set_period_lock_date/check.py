"""Postcondition checks for account.lock_books_set_period_lock_date.

Validates:
1. The main company exists.
2. Its `fiscalyear_lock_date` (Non-Advisors / Global Lock Date) is exactly
   date(2026, 3, 31).
3. None of the other lock-date fields were changed (still False).
"""

from datetime import date


EXPECTED = date(2026, 3, 31)


def _main_company(env):
    return env.ref("base.main_company", raise_if_not_found=False) or env["res.company"].search(
        [], order="id asc", limit=1
    )


def check(env):
    failures = []

    company = _main_company(env)
    if not company:
        return ["No res.company record found"]

    if company.fiscalyear_lock_date != EXPECTED:
        failures.append(
            f"Company '{company.name}' fiscalyear_lock_date is "
            f"{company.fiscalyear_lock_date!r}, expected {EXPECTED!r}"
        )

    # Make sure the agent did not flip a different lock-date variant by
    # mistake (the prompt is specific that only the Non-Advisors / Global
    # Lock Date should change).
    for field_name in ("tax_lock_date", "sale_lock_date", "purchase_lock_date", "hard_lock_date"):
        value = getattr(company, field_name, False)
        if value:
            failures.append(
                f"Company '{company.name}' {field_name} should be unset, "
                f"found {value!r}"
            )

    return failures
