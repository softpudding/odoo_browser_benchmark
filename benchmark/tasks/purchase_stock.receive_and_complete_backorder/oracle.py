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
    """Set the Done quantity on a stock move line row inside a picking form."""
    # Use the form's list renderer (not top-level list view)
    row = page.locator(
        ".o_form_view .o_list_renderer .o_data_row, "
        ".o_list_view .o_data_row"
    ).nth(row_index)
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

    # Click "Receive" to open the receipt (button string is "Receive", not "Receive Products")
    receive_btn = page.locator(
        ".o_statusbar_buttons button:visible:has-text('Receive'), "
        "button[name='action_view_picking']:visible"
    ).first
    receive_btn.click()
    page.wait_for_load_state("load")
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
    page.wait_for_timeout(1500)
    _wait_no_loading(page)

    # In the backorder dialog, click "Create Backorder"
    modal = page.locator(".modal:visible")
    if modal.count() > 0:
        modal.last.locator("button:has-text('Create Backorder')").first.click()
        page.wait_for_timeout(1500)
        _wait_no_loading(page)
        _wait_for_ready(page)

    # Navigate back to the PO to find the backorder receipt
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
    ready_row = page.locator(
        ".o_list_view .o_data_row:has-text('Ready'), "
        ".o_list_view .o_data_row:has-text('Assigned')"
    )
    if ready_row.count() > 0:
        ready_row.first.click()
    else:
        # Try clicking the second row (first is Done, second is the backorder)
        rows = page.locator(".o_list_view .o_data_row")
        if rows.count() > 1:
            rows.nth(1).click()
        else:
            rows.first.click()
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

    # Handle any dialog that appears
    modal = page.locator(".modal:visible")
    if modal.count() > 0:
        modal.last.locator(
            "button:has-text('Ok'), button.btn-primary"
        ).first.click()
        page.wait_for_timeout(1000)
        _wait_no_loading(page)


run_oracle(oracle)
