"""Oracle for hr_expense.refuse_report_with_reason_chatter.

Open INVOICE-MISMATCH-2026 expense, click Refuse on the statusbar,
type the refusal reason in the wizard dialog, confirm. Verify the
expense is in the 'refused' state and the reason is posted to chatter.
"""

from benchmark.oracle_helpers import (
    click_list_row,
    login,
    navigate,
    run_oracle,
    _wait_no_loading,
)


REASON = "Receipt amount doesn't match invoice — please resubmit"


def oracle(page):
    login(page)
    navigate(page, "/odoo/expenses")
    _wait_no_loading(page)
    page.wait_for_timeout(1200)

    # Approver view: all expenses (Odoo 19 uses hr.expense directly).
    navigate(
        page,
        "/odoo/action-hr_expense.hr_expense_actions_my_all",
    )
    _wait_no_loading(page)
    page.wait_for_timeout(1000)

    # Clear any default filters so the submitted expense is visible.
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

    click_list_row(page, "INVOICE-MISMATCH-2026")
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
    textarea = page.locator(
        ".modal textarea:visible, .modal input[type='text']:visible"
    )
    if textarea.count() > 0:
        textarea.first.click()
        textarea.first.fill(REASON)
        page.wait_for_timeout(300)

    # Confirm refuse.
    confirm = page.locator(
        ".modal button.btn-primary:visible, "
        ".modal footer button:has-text('Refuse'):visible, "
        ".modal footer button:has-text('Send'):visible"
    )
    confirm.first.click()
    page.wait_for_timeout(1500)
    _wait_no_loading(page)


run_oracle(oracle)
