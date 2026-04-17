"""Oracle for hr_expense.approve_submitted_report.

Open Expenses to Process, find 'Alpha project travel 2026', approve it.
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
    navigate(page, "/odoo/expenses-to-process")
    _wait_no_loading(page)
    page.wait_for_timeout(1200)

    # Ensure list view.
    list_btn = page.locator("button[data-tooltip='List']:visible")
    if list_btn.count() > 0:
        list_btn.first.click()
        page.wait_for_timeout(500)
        _wait_no_loading(page)

    # Remove default filter facets that might hide the submitted expenses
    # (e.g., the 'My Team' default) so that Priya's record is visible.
    # Keep the "Submitted" filter by default — it's helpful.
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

    click_list_row(page, "Alpha project travel 2026")
    page.wait_for_timeout(800)
    _wait_for_ready(page)

    # Approve via header/statusbar.
    approve_btn = page.locator(
        ".o_form_statusbar button[name='action_approve']:visible"
    )
    if approve_btn.count() > 0:
        approve_btn.first.click()
    else:
        any_approve = page.locator(
            "button[name='action_approve']:visible"
        )
        if any_approve.count() > 0:
            any_approve.first.click()
        else:
            page.locator(
                "button:has-text('Approve'):visible"
            ).first.click()

    page.wait_for_timeout(1500)
    _wait_no_loading(page)


run_oracle(oracle)
