"""Oracle for sale.confirm_correct_order.

Open Sales. Find the Gemini Furniture quotation that has BOTH
Standing Desk AND Office Chair on the same order. Confirm only that one.
"""

from benchmark.oracle_helpers import (
    click_breadcrumb,
    click_list_row,
    click_status_button,
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

    # We need to find the quotation with both Standing Desk and Office Chair.
    # Get all Gemini Furniture rows and check each one.
    rows = page.locator(".o_list_view .o_data_row:has-text('Gemini Furniture')")
    row_count = rows.count()

    found = False
    for i in range(row_count):
        # Navigate fresh each time to get clean list
        navigate(page, "/odoo/sales")
        _wait_no_loading(page)

        rows = page.locator(".o_list_view .o_data_row:has-text('Gemini Furniture')")
        rows.nth(i).click()
        page.wait_for_load_state("load")
        _wait_for_ready(page)
        page.wait_for_timeout(1000)

        # Check if this order has both Standing Desk and Office Chair
        body = page.locator(".o_form_view").inner_text()
        has_standing = "Standing Desk" in body
        has_chair = "Office Chair" in body

        if has_standing and has_chair:
            # This is the correct one - confirm it
            click_status_button(page, "Confirm")
            page.wait_for_timeout(1000)
            _wait_no_loading(page)

            # Handle any confirmation dialog
            modal = page.locator(".modal:visible")
            if modal.count() > 0:
                modal.last.locator(
                    "button:has-text('Ok'), button.btn-primary"
                ).first.click()
                page.wait_for_timeout(1000)
                _wait_no_loading(page)

            found = True
            break

    if not found:
        raise Exception("Could not find quotation with both Standing Desk and Office Chair")


run_oracle(oracle)
