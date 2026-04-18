"""Oracle for hr_holidays.approve_leave_as_manager.

Navigate to the manager approval queue, open the pending "Family event
leave" request from Marc Demo, and click Approve on the statusbar so the
leave transitions to state=validate.
"""

from benchmark.oracle_helpers import (
    click_list_row,
    login,
    navigate,
    run_oracle,
    _wait_no_loading,
)


LEAVE_NAME = "Family event leave"


def oracle(page):
    login(page)
    # Manager approval view
    navigate(page, "/odoo/time-off-approval")
    _wait_no_loading(page)
    page.wait_for_timeout(1500)

    # Switch to list view if buttons exist
    list_btn = page.locator("button[data-tooltip='List']:visible")
    if list_btn.count() > 0:
        list_btn.first.click()
        page.wait_for_timeout(800)
        _wait_no_loading(page)

    # Remove any default search facets so the pending leave is visible
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

    # Open the pending request
    click_list_row(page, LEAVE_NAME)
    page.wait_for_timeout(1000)
    _wait_no_loading(page)

    # Click the Approve action button on the statusbar. Prefer the
    # technical name selector; fall back to text-based lookup.
    approve_btn = page.locator(
        ".o_form_statusbar button[name='action_approve']:visible"
    )
    if approve_btn.count() > 0:
        approve_btn.first.click()
    else:
        any_approve = page.locator("button[name='action_approve']:visible")
        if any_approve.count() > 0:
            any_approve.first.click()
        else:
            page.locator(
                "button:has-text('Approve'):visible, "
                "button:has-text('Validate'):visible"
            ).first.click()
    page.wait_for_timeout(1500)
    _wait_no_loading(page)

    # Some configurations (double validation) show a second Validate step.
    # Click it if it appears so the leave reaches state=validate.
    validate_btn = page.locator(
        ".o_form_statusbar button[name='action_validate']:visible"
    )
    if validate_btn.count() > 0:
        validate_btn.first.click()
        page.wait_for_timeout(1500)
        _wait_no_loading(page)


run_oracle(oracle)
