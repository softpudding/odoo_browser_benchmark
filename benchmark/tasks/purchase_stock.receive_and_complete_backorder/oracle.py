"""Oracle for purchase_stock.receive_and_complete_backorder.

Find confirmed PO from Stellar Supplies with origin BENCH-PARTIAL.
Batch 1: Receive partial quantities (Copper Wire Spool=4, Steel Bracket=8),
validate, and create backorder.
Batch 2: Open the backorder receipt and receive remaining quantities
(Copper Wire Spool=6, Steel Bracket=12), then validate.
"""

from benchmark.oracle_helpers import (
    click_button,
    click_list_row,
    click_stat_button,
    click_status_button,
    login,
    modal_click_button,
    navigate,
    run_oracle,
    _wait_no_loading,
    _wait_for_ready,
)


def _set_done_qty(page, row_index, value):
    """Set the Done quantity on a stock move line row."""
    row = page.locator(".o_list_view .o_data_row").nth(row_index)
    # The done quantity field is named 'quantity' in stock.move
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

    # Find and open the PO with origin BENCH-PARTIAL
    click_list_row(page, "BENCH-PARTIAL")
    page.wait_for_timeout(1000)

    # Click "Receive Products" to open the receipt
    click_status_button(page, "Receive Products")
    page.wait_for_timeout(1000)
    _wait_no_loading(page)
    _wait_for_ready(page)

    # Batch 1: Set partial done quantities
    # Copper Wire Spool: 4 (demand is 10)
    _set_done_qty(page, 0, "4")
    page.wait_for_timeout(500)

    # Steel Bracket: 8 (demand is 20)
    _set_done_qty(page, 1, "8")
    page.wait_for_timeout(500)

    # Validate the receipt
    click_button(page, "Validate")
    page.wait_for_timeout(1000)
    _wait_no_loading(page)

    # In the backorder dialog, click "Create Backorder"
    modal_click_button(page, "Create Backorder")
    page.wait_for_timeout(1000)
    _wait_no_loading(page)
    _wait_for_ready(page)

    # Navigate back to the PO to find the backorder receipt
    # Use breadcrumb or navigate back to purchase
    navigate(page, "/odoo/purchase")
    _wait_no_loading(page)

    # Reopen the PO
    click_list_row(page, "BENCH-PARTIAL")
    page.wait_for_timeout(1000)

    # Click the Receipt smart button to see all receipts
    click_stat_button(page, "Receipt")
    page.wait_for_timeout(1000)
    _wait_no_loading(page)
    _wait_for_ready(page)

    # Find the backorder (the one that is not done - should be in "Ready" or "Assigned" state)
    # Click the row that shows Ready/Assigned status (the pending one)
    ready_row = page.locator(".o_list_view .o_data_row:has-text('Ready'), .o_list_view .o_data_row:has-text('Assigned')").first
    ready_row.click()
    page.wait_for_load_state("load")
    _wait_for_ready(page)
    page.wait_for_timeout(1000)

    # Batch 2: Set remaining done quantities to full demand
    # Copper Wire Spool: 6 (remaining demand)
    _set_done_qty(page, 0, "6")
    page.wait_for_timeout(500)

    # Steel Bracket: 12 (remaining demand)
    _set_done_qty(page, 1, "12")
    page.wait_for_timeout(500)

    # Validate the backorder receipt
    click_button(page, "Validate")
    page.wait_for_timeout(1000)
    _wait_no_loading(page)


run_oracle(oracle)
