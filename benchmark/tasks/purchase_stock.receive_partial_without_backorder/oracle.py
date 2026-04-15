"""Oracle for purchase_stock.receive_partial_without_backorder.

Find confirmed PO from North Coast Components with origin NOBACK-04.
Open receipt, set partial done quantities (Servo Motor=6, Sensor Harness=9),
validate, and choose "No Backorder" in the backorder dialog.
"""

from benchmark.oracle_helpers import (
    click_button,
    click_list_row,
    click_status_button,
    login,
    modal_click_button,
    navigate,
    run_oracle,
    _wait_no_loading,
    _wait_for_ready,
)


def _set_done_qty(page, row_index, value):
    """Set the Done quantity on a stock move line row inside a picking form."""
    row = page.locator(
        ".o_form_view .o_list_renderer .o_data_row, "
        ".o_list_view .o_data_row"
    ).nth(row_index)
    cell = row.locator("td[name='quantity'], .o_field_widget[name='quantity']").first
    cell.click()
    page.wait_for_timeout(300)
    inp = cell.locator("input").first
    inp.fill("")
    inp.fill(value)
    inp.press("Tab")
    page.wait_for_timeout(500)
    _wait_no_loading(page)


def oracle(page):
    login(page)
    navigate(page, "/odoo/purchase")
    _wait_no_loading(page)

    # Find and open the PO with origin NOBACK-04
    click_list_row(page, "NOBACK-04")
    page.wait_for_timeout(1000)

    # Click "Receive" to open the receipt (button text is "Receive", not "Receive Products")
    receive_btn = page.locator(
        ".o_statusbar_buttons button:visible:has-text('Receive'), "
        "button[name='action_view_picking']:visible"
    ).first
    receive_btn.click()
    page.wait_for_load_state("load")
    page.wait_for_timeout(1000)
    _wait_no_loading(page)
    _wait_for_ready(page)

    # Set partial done quantities
    # Servo Motor: 6 (demand is 8)
    _set_done_qty(page, 0, "6")
    page.wait_for_timeout(500)

    # Sensor Harness: 9 (demand is 12)
    _set_done_qty(page, 1, "9")
    page.wait_for_timeout(500)

    # Validate the receipt
    click_button(page, "Validate")
    page.wait_for_timeout(1500)
    _wait_no_loading(page)

    # In the backorder dialog, choose "No Backorder"
    modal = page.locator(".modal:visible")
    if modal.count() > 0:
        modal.last.locator("button:has-text('No Backorder')").first.click()
        page.wait_for_timeout(1000)
        _wait_no_loading(page)


run_oracle(oracle)
