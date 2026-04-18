"""Oracle for hr_expense.post_approved_expense_to_journal.

Open 'Bench Taxi Fare' (approved expense), click 'Post Journal Entries'
on the statusbar, confirm the Post Expenses wizard by clicking the
'Post Expenses' footer button with the default journal and accounting
date. Verify the expense transitions to the 'posted' state and that an
account.move is linked.
"""

from benchmark.oracle_helpers import (
    click_list_row,
    login,
    navigate,
    run_oracle,
    _wait_no_loading,
    _wait_for_ready,
)


def oracle(page):
    login(page)
    navigate(page, "/odoo/expenses")
    _wait_no_loading(page)
    page.wait_for_timeout(1200)

    # "All Expenses" list — shows every state regardless of filters.
    navigate(
        page,
        "/odoo/action-hr_expense.hr_expense_actions_my_all",
    )
    _wait_no_loading(page)
    page.wait_for_timeout(1200)

    # Drop any default filter facets so the approved expense is visible.
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

    # Switch to list view if we landed on kanban.
    list_btn = page.locator("button[data-tooltip='List']:visible")
    if list_btn.count() > 0:
        try:
            list_btn.first.click()
            page.wait_for_timeout(500)
            _wait_no_loading(page)
        except Exception:
            pass

    click_list_row(page, "Bench Taxi Fare")
    page.wait_for_timeout(1000)
    _wait_for_ready(page)
    _wait_no_loading(page)

    # Click 'Post Journal Entries' on the statusbar.
    post_btn = page.locator(
        ".o_form_statusbar button[name='action_post']:visible"
    )
    if post_btn.count() == 0:
        post_btn = page.locator(
            "button[name='action_post']:visible"
        )
    if post_btn.count() == 0:
        post_btn = page.locator(
            "button:has-text('Post Journal Entries'):visible"
        )
    post_btn.first.click()
    page.wait_for_timeout(1500)
    _wait_no_loading(page)

    # Confirm the Post Expenses wizard dialog.
    confirm = page.locator(
        ".modal footer button[name='action_post_entry']:visible"
    )
    if confirm.count() == 0:
        confirm = page.locator(
            ".modal footer button:has-text('Post Expenses'):visible"
        )
    if confirm.count() == 0:
        confirm = page.locator(
            ".modal button.btn-primary:visible"
        )
    confirm.first.click()

    page.wait_for_timeout(2000)
    _wait_no_loading(page)


run_oracle(oracle)
