"""Oracle for hr_holidays.cancel_approved_leave_and_reallocate.

Refuse the approved 'Family vacation (tentative)' leave.
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
    navigate(page, "/odoo/action-hr_holidays.hr_leave_action_action_approve_department")
    _wait_no_loading(page)
    page.wait_for_timeout(1500)

    # Clear filters so validated leaves are visible.
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
    list_btn = page.locator("button[data-tooltip='List']:visible")
    if list_btn.count() > 0:
        list_btn.first.click()
        page.wait_for_timeout(500)

    click_list_row(page, "Family vacation (tentative)")
    page.wait_for_timeout(800)
    _wait_no_loading(page)

    refuse_btn = page.locator(
        ".o_form_statusbar button[name='action_refuse']:visible"
    )
    refuse_btn.first.click()
    page.wait_for_timeout(1500)
    _wait_no_loading(page)


run_oracle(oracle)
