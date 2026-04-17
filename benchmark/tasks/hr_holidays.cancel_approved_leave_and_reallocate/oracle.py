"""Oracle for hr_holidays.cancel_approved_leave_and_reallocate.

Refuse the approved Family vacation (tentative) leave, then create a
new Approved leave for the corrected dates.
"""

from benchmark.oracle_helpers import (
    click_list_row,
    fill_text_field,
    login,
    navigate,
    run_oracle,
    save_form,
    set_date,
    set_many2one,
    _wait_no_loading,
)


def oracle(page):
    login(page)
    navigate(page, "/odoo/action-hr_holidays.hr_leave_action_action_approve_department")
    _wait_no_loading(page)
    page.wait_for_timeout(1500)

    # Clear filters to see all leaves.
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

    # Switch to list view if not already.
    list_btn = page.locator("button[data-tooltip='List']:visible")
    if list_btn.count() > 0:
        list_btn.first.click()
        page.wait_for_timeout(500)

    click_list_row(page, "Family vacation (tentative)")
    page.wait_for_timeout(800)
    _wait_no_loading(page)

    # Click Refuse.
    refuse_btn = page.locator(
        ".o_form_statusbar button[name='action_refuse']:visible"
    )
    refuse_btn.first.click()
    page.wait_for_timeout(1000)
    _wait_no_loading(page)

    # Back to list.
    navigate(page, "/odoo/time-off-approval")
    _wait_no_loading(page)
    page.wait_for_timeout(1000)

    # Clear filters again.
    for _ in range(5):
        facets = page.locator(".o_searchview .o_facet_remove:visible")
        if facets.count() == 0:
            break
        try:
            facets.first.click()
            page.wait_for_timeout(300)
        except Exception:
            break

    # Click New.
    new_btn = page.locator(
        "button.o_list_button_add:visible, "
        ".o_control_panel_main_buttons button:has-text('New'):visible"
    )
    new_btn.first.click()
    page.wait_for_timeout(800)
    _wait_no_loading(page)

    # Fill: employee, leave type, dates, description.
    set_many2one(page, "employee_id", "Marc Demo")
    set_many2one(page, "holiday_status_id", "Paid Time Off")
    set_date(page, "request_date_from", "07/13/2026")
    set_date(page, "request_date_to", "07/17/2026")
    fill_text_field(page, "name", "Family vacation (confirmed)")

    save_form(page)
    page.wait_for_timeout(1200)
    _wait_no_loading(page)

    # Approve the new request.
    approve_btn = page.locator(
        ".o_form_statusbar button[name='action_approve']:visible, "
        ".o_form_statusbar button[name='action_validate']:visible"
    )
    if approve_btn.count() > 0:
        approve_btn.first.click()
        page.wait_for_timeout(1200)
        _wait_no_loading(page)


run_oracle(oracle)
