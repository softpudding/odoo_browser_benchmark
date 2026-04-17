"""Oracle for hr_expense.reject_expense_report_with_feedback.

Open the SUMMIT-2026 report, click Refuse, fill the reason, confirm.
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

    # Go to the approver view of hr.expense (Odoo 19 uses hr.expense
    # directly; the old hr.expense.sheet is gone).
    navigate(
        page,
        "/odoo/action-hr_expense.hr_expense_actions_my_all",
    )
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

    click_list_row(page, "SUMMIT-2026")
    page.wait_for_timeout(800)
    _wait_no_loading(page)

    # Click Refuse statusbar button.
    refuse_btn = page.locator(
        ".o_form_statusbar button[name='action_refuse']:visible, "
        ".o_form_statusbar button:has-text('Refuse'):visible"
    )
    refuse_btn.first.click()
    page.wait_for_timeout(800)

    # Modal asks for reason.
    reason = (
        "Hotel rate exceeds company cap — please resubmit with itemised "
        "receipts under $200/night."
    )
    textarea = page.locator(".modal textarea:visible, .modal input[type='text']:visible")
    if textarea.count() > 0:
        textarea.first.click()
        textarea.first.fill(reason)
        page.wait_for_timeout(300)

    # Confirm refuse (button labelled "Refuse" or "Send" in modal).
    confirm = page.locator(
        ".modal button.btn-primary:visible, "
        ".modal button:has-text('Refuse'):visible, "
        ".modal button:has-text('Send'):visible"
    )
    confirm.first.click()
    page.wait_for_timeout(1500)
    _wait_no_loading(page)


run_oracle(oracle)
