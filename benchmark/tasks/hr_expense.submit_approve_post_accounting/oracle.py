"""Oracle for hr_expense.submit_approve_post_accounting.

Submit → Approve → Post to accounting a draft expense report.
"""

from benchmark.oracle_helpers import (
    click_list_row,
    login,
    navigate,
    run_oracle,
    _wait_no_loading,
)


def oracle(page):
    login(page)
    navigate(page, "/odoo/expenses")
    _wait_no_loading(page)
    page.wait_for_timeout(1200)

    # Odoo 19: hr.expense direct action (no more hr.expense.sheet).
    navigate(page, "/odoo/action-hr_expense.hr_expense_actions_my_all")
    _wait_no_loading(page)
    page.wait_for_timeout(1200)

    # Clear filters.
    for _ in range(5):
        facets = page.locator(".o_searchview .o_facet_remove:visible")
        if facets.count() == 0:
            break
        try:
            facets.first.click()
            page.wait_for_timeout(300)
        except Exception:
            break
    _wait_no_loading(page)

    click_list_row(page, "TRV-2026-04")
    page.wait_for_timeout(800)
    _wait_no_loading(page)

    # 1. Submit.
    submit_btn = page.locator(
        ".o_form_statusbar button[name='action_submit']:visible, "
        ".o_form_statusbar button:has-text('Submit'):visible"
    )
    submit_btn.first.click()
    page.wait_for_timeout(1200)
    _wait_no_loading(page)

    # 2. Approve.
    approve_btn = page.locator(
        ".o_form_statusbar button[name='action_approve']:visible, "
        ".o_form_statusbar button:has-text('Approve'):visible"
    )
    approve_btn.first.click()
    page.wait_for_timeout(2000)
    _wait_no_loading(page)

    # Reload the form to ensure the Post button appears (it is only
    # shown once state transitions to 'approved').
    page.reload()
    _wait_no_loading(page)
    page.wait_for_timeout(1500)

    # 3. Post Journal Entries.
    post_btn = page.locator(
        ".o_form_statusbar button[name='action_post'], "
        "button[name='action_post']:visible"
    ).first
    post_btn.wait_for(state="visible", timeout=15000)
    post_btn.click()
    page.wait_for_timeout(2000)
    _wait_no_loading(page)


run_oracle(oracle)
