"""Oracle for sale_stock.confirm_order_deliver_partial_backorder.

Confirm quotation BENCH-SO-BACK, navigate to the delivery, set partial
done quantities (15/25, 40/40, 6/20), validate, and create a backorder.
"""

from benchmark.oracle_helpers import (
    clear_search_filters,
    click_button,
    click_list_row,
    click_stat_button,
    click_status_button,
    login,
    modal_click_button,
    navigate,
    run_oracle,
    set_o2m_field,
    _wait_no_loading,
    _wait_for_ready,
)


def oracle(page):
    login(page)
    navigate(page, "/odoo/sales")
    _wait_no_loading(page)

    # Remove default "My Quotations" filter so we can see BENCH-SO-BACK
    clear_search_filters(page)
    _wait_no_loading(page)

    # Open the quotation — search by customer name since ref may not be visible
    click_list_row(page, "Westfield Manufacturing")
    page.wait_for_timeout(1000)
    _wait_no_loading(page)

    # Confirm the quotation to convert it to a Sales Order
    click_status_button(page, "Confirm")
    page.wait_for_timeout(1500)
    _wait_no_loading(page)

    # Handle any confirmation dialog
    modal = page.locator(".modal:visible")
    if modal.count() > 0:
        modal.last.locator(
            "button:has-text('Ok'), button.btn-primary"
        ).first.click()
        page.wait_for_timeout(1000)
        _wait_no_loading(page)

    # Click the Delivery smart button
    click_stat_button(page, "Delivery")
    page.wait_for_timeout(1000)
    _wait_no_loading(page)
    _wait_for_ready(page)

    # Set partial done quantities on stock move lines
    # Row 0: Precision Bearing Kit -> 15 (out of 25)
    set_o2m_field(page, 0, "quantity", "15")
    page.wait_for_timeout(500)

    # Row 1: Stainless Steel Rod 2m -> 40 (out of 40)
    set_o2m_field(page, 1, "quantity", "40")
    page.wait_for_timeout(500)

    # Row 2: Titanium Bolt Set M12 -> 6 (out of 20)
    set_o2m_field(page, 2, "quantity", "6")
    page.wait_for_timeout(500)

    # Validate the delivery
    click_button(page, "Validate")
    page.wait_for_timeout(1500)
    _wait_no_loading(page)

    # In the backorder dialog, click "Create Backorder"
    modal = page.locator(".modal:visible")
    if modal.count() > 0:
        modal.last.locator("button:has-text('Create Backorder')").first.click()
        page.wait_for_timeout(1500)
        _wait_no_loading(page)


run_oracle(oracle)
