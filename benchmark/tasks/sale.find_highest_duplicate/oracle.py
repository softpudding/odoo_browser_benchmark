"""Oracle for sale.find_highest_duplicate.

Azure Interior has highest confirmed total ($1600).
Among Azure's drafts, the smallest is $280 (Monitor Arm, Whiteboard, Desk Lamp).
Find and duplicate that quotation.
"""

from benchmark.oracle_helpers import (
    click_button,
    click_list_row,
    login,
    navigate,
    run_oracle,
    _wait_no_loading,
    _wait_for_ready,
)


def oracle(page):
    login(page)
    navigate(page, "/odoo/sales")
    _wait_no_loading(page)

    # Remove "My Quotations" filter to see all quotations
    # Click the X on any active filter tag
    filter_tags = page.locator(".o_searchview .o_facet_remove, .o_searchview_facet .o_facet_remove")
    while filter_tags.count() > 0:
        filter_tags.first.click()
        page.wait_for_timeout(500)
        filter_tags = page.locator(".o_searchview .o_facet_remove, .o_searchview_facet .o_facet_remove")

    _wait_no_loading(page)
    page.wait_for_timeout(500)

    # Find Azure Interior's draft with amount $280
    # The $280 draft has Monitor Arm, Whiteboard, Desk Lamp
    # We need to find the right row. Look for Azure Interior rows.
    rows = page.locator(".o_list_view .o_data_row:has-text('Azure Interior')")
    row_count = rows.count()

    found = False
    for i in range(row_count):
        # Re-navigate each time
        navigate(page, "/odoo/sales")
        _wait_no_loading(page)

        # Remove filters again
        filter_tags = page.locator(".o_searchview .o_facet_remove, .o_searchview_facet .o_facet_remove")
        while filter_tags.count() > 0:
            filter_tags.first.click()
            page.wait_for_timeout(500)
            filter_tags = page.locator(".o_searchview .o_facet_remove, .o_searchview_facet .o_facet_remove")
        _wait_no_loading(page)
        page.wait_for_timeout(500)

        rows = page.locator(".o_list_view .o_data_row:has-text('Azure Interior')")
        rows.nth(i).click()
        page.wait_for_load_state("load")
        _wait_for_ready(page)
        page.wait_for_timeout(1000)

        # Check if this is a draft with Monitor Arm (identifies the $280 order)
        body = page.locator(".o_form_view").inner_text()
        has_monitor_arm = "Monitor Arm" in body
        has_whiteboard = "Whiteboard" in body
        # Check it's a draft (Quotation status)
        is_draft = "Quotation" in page.locator(".o_statusbar_status").inner_text()

        if has_monitor_arm and has_whiteboard:
            # This is the $280 draft - duplicate it
            # Use Action menu > Duplicate
            page.locator(".o_cp_action_menus button, button:has-text('Action')").first.click()
            page.wait_for_timeout(500)

            page.locator(".dropdown-menu .dropdown-item:has-text('Duplicate')").first.click()
            page.wait_for_timeout(1000)
            _wait_no_loading(page)

            found = True
            break

    if not found:
        raise Exception("Could not find Azure Interior draft with $280 total")


run_oracle(oracle)
