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

    # Go to My Expense Reports.
    navigate(page, "/odoo/action-hr_expense.action_hr_expense_sheet_my_all")
    _wait_no_loading(page)
    page.wait_for_timeout(1000)

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
        ".o_form_statusbar button[name='action_submit_sheet']:visible, "
        ".o_form_statusbar button:has-text('Submit'):visible"
    )
    submit_btn.first.click()
    page.wait_for_timeout(1200)
    _wait_no_loading(page)

    # 2. Approve.
    approve_btn = page.locator(
        ".o_form_statusbar button[name='action_approve_expense_sheets']:visible, "
        ".o_form_statusbar button:has-text('Approve'):visible"
    )
    approve_btn.first.click()
    page.wait_for_timeout(1200)
    _wait_no_loading(page)

    # 3. Post to accounting — button may be 'Post Journal Entries'.
    post_btn = page.locator(
        ".o_form_statusbar button[name='action_sheet_move_post']:visible, "
        ".o_form_statusbar button[name='action_sheet_move_create']:visible, "
        ".o_form_statusbar button:has-text('Post Journal Entries'):visible, "
        ".o_form_statusbar button:has-text('Post'):visible"
    )
    post_btn.first.click()
    page.wait_for_timeout(1500)
    _wait_no_loading(page)


run_oracle(oracle)
