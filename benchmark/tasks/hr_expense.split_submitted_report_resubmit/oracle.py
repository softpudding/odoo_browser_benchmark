"""Oracle for hr_expense.split_submitted_report_resubmit.

Drives the manager approval workflow via the UI:
1. Navigate to the expenses app, clear filters.
2. Open the R-BENCH-SPLIT-001 Gadget expense and click Refuse; fill the
   reason 'Not compliant' and confirm the modal.
3. Go back, open the Meal expense and click Approve.
4. Go back, open the Taxi expense and click Approve.
"""

from benchmark.oracle_helpers import (
    click_list_row,
    login,
    navigate,
    run_oracle,
    _wait_no_loading,
)


MEAL_NAME = "R-BENCH-SPLIT-001 Meal"
GADGET_NAME = "R-BENCH-SPLIT-001 Gadget"
TAXI_NAME = "R-BENCH-SPLIT-001 Taxi"
REFUSE_REASON = "Not compliant"


def _clear_filters(page):
    for _ in range(6):
        facets = page.locator(".o_searchview .o_facet_remove:visible")
        if facets.count() == 0:
            break
        try:
            facets.first.click()
            page.wait_for_timeout(250)
        except Exception:
            break
    _wait_no_loading(page)


def _open_approver_list(page):
    navigate(page, "/odoo/action-hr_expense.hr_expense_actions_my_all")
    _wait_no_loading(page)
    page.wait_for_timeout(800)
    _clear_filters(page)
    page.wait_for_timeout(400)


def _open_expense(page, text):
    _open_approver_list(page)
    click_list_row(page, text)
    page.wait_for_timeout(800)
    _wait_no_loading(page)


def _refuse(page, text, reason):
    _open_expense(page, text)

    refuse_btn = page.locator(
        ".o_form_statusbar button[name='action_refuse']:visible, "
        ".o_form_statusbar button:has-text('Refuse'):visible"
    )
    refuse_btn.first.click()
    page.wait_for_timeout(800)

    textarea = page.locator(
        ".modal textarea:visible, "
        ".modal input[type='text']:visible, "
        ".modal .o_field_widget[name='reason'] input:visible, "
        ".modal .o_field_widget[name='reason'] textarea:visible"
    )
    if textarea.count() > 0:
        textarea.first.click()
        textarea.first.fill(reason)
        page.wait_for_timeout(300)

    confirm = page.locator(
        ".modal button[name='action_refuse']:visible, "
        ".modal button.btn-primary:visible, "
        ".modal button:has-text('Refuse Expense'):visible, "
        ".modal button:has-text('Refuse'):visible"
    )
    confirm.first.click()
    page.wait_for_timeout(1500)
    _wait_no_loading(page)


def _approve(page, text):
    _open_expense(page, text)

    approve_btn = page.locator(
        ".o_form_statusbar button[name='action_approve']:visible, "
        ".o_form_statusbar button:has-text('Approve'):visible"
    )
    approve_btn.first.click()
    page.wait_for_timeout(1500)
    _wait_no_loading(page)

    # If a duplicate-confirmation wizard appears, just confirm it.
    modal_confirm = page.locator(
        ".modal button.btn-primary:visible, "
        ".modal button:has-text('Approve'):visible, "
        ".modal button:has-text('Ok'):visible"
    )
    if modal_confirm.count() > 0:
        try:
            modal_confirm.first.click()
            page.wait_for_timeout(800)
            _wait_no_loading(page)
        except Exception:
            pass


def oracle(page):
    login(page)
    navigate(page, "/odoo/expenses")
    _wait_no_loading(page)
    page.wait_for_timeout(1000)

    _refuse(page, GADGET_NAME, REFUSE_REASON)
    _approve(page, MEAL_NAME)
    _approve(page, TAXI_NAME)


run_oracle(oracle)
