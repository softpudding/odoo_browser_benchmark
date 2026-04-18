"""Seed for account.lock_books_set_period_lock_date.

Idempotent reset: clear any prior lock date on the main company so the task
starts from an unset (False) Non-Advisors / Global Lock Date.
"""


def _main_company(env):
    return env.ref("base.main_company", raise_if_not_found=False) or env["res.company"].search(
        [], order="id asc", limit=1
    )


def setup(env):
    company = _main_company(env)
    if not company:
        return
    # Reset only the soft fiscal-year (global / non-advisors) lock date.
    # Do NOT touch hard_lock_date (irreversible) — but if a previous failed
    # run somehow set it, leave it alone here; this seed only governs the
    # field the task is about.
    if company.fiscalyear_lock_date:
        company.sudo().write({"fiscalyear_lock_date": False})
