"""Cleanup for account.lock_books_set_period_lock_date.

Reset the Non-Advisors / Global Lock Date on the main company so subsequent
runs (or other tasks that rely on an unlocked accounting period) start
clean.
"""


def _main_company(env):
    return env.ref("base.main_company", raise_if_not_found=False) or env["res.company"].search(
        [], order="id asc", limit=1
    )


def cleanup(env):
    company = _main_company(env)
    if not company:
        return
    if company.fiscalyear_lock_date:
        company.sudo().write({"fiscalyear_lock_date": False})
