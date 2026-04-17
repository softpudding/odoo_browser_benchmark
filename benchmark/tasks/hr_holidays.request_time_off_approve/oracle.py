"""Oracle for hr_holidays.request_time_off_approve.

Navigate to the manager approval view, find the pending Sick Time Off
request, open it in form view, and approve it.
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
    # Navigate to the manager's time-off approval view
    navigate(page, "/odoo/time-off-approval")
    _wait_no_loading(page)
    page.wait_for_timeout(1500)

    # Switch to list view
    list_btn = page.locator("button[data-tooltip='List']:visible")
    if list_btn.count() > 0:
        list_btn.first.click()
        page.wait_for_timeout(800)
        _wait_no_loading(page)

    # Remove default search filters to show all leaves
    for _ in range(5):
        facets = page.locator(".o_searchview .o_facet_remove:visible")
        if facets.count() == 0:
            break
        try:
            facets.first.click()
            page.wait_for_timeout(400)
        except Exception:
            break
    _wait_no_loading(page)
    page.wait_for_timeout(500)

    # Find and click on the leave request
    click_list_row(page, "Medical appointment recovery")
    page.wait_for_timeout(800)
    _wait_no_loading(page)

    # Now in form view — the Approve button is in the statusbar
    # In Odoo, <header> renders as <div class="o_form_statusbar">
    approve_btn = page.locator(
        ".o_form_statusbar button[name='action_approve']:visible"
    )
    if approve_btn.count() > 0:
        approve_btn.first.click()
    else:
        # Try any visible approve button on the page
        any_approve = page.locator("button[name='action_approve']:visible")
        if any_approve.count() > 0:
            any_approve.first.click()
        else:
            # Last resort: try "Approve" or "Validate" text
            page.locator(
                "button:has-text('Approve'):visible, "
                "button:has-text('Validate'):visible"
            ).first.click()
    page.wait_for_timeout(1500)
    _wait_no_loading(page)


run_oracle(oracle)
