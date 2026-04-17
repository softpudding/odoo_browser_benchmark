"""Oracle for stock.receive_serial_tracked_product."""

from benchmark.oracle_helpers import (
    click_list_row,
    clear_search_filters,
    ensure_list_view,
    login,
    navigate,
    run_oracle,
    _wait_no_loading,
)


SERIALS = ["CSX-001", "CSX-002", "CSX-003"]


def oracle(page):
    login(page)
    navigate(page, "/odoo/inventory")
    _wait_no_loading(page)
    page.wait_for_timeout(1000)

    # Click Receipts from overview
    receipts_link = page.locator('.o_kanban_record a:has-text("Receipts")')
    if receipts_link.count() > 0:
        receipts_link.first.click()
    else:
        page.locator('.o_kanban_record:has-text("Receipts")').first.click()
    page.wait_for_timeout(3000)
    _wait_no_loading(page)

    page.wait_for_selector(
        ".o_list_view .o_data_row, .o_kanban_record, .o_nocontent_help",
        timeout=15000,
    )

    clear_search_filters(page)
    page.wait_for_timeout(1000)
    _wait_no_loading(page)

    ensure_list_view(page)
    page.wait_for_timeout(1000)

    click_list_row(page, "BENCH-SERIAL-REC-01")
    page.wait_for_timeout(1000)
    _wait_no_loading(page)

    # Click "Details" on the move line to open detailed operations modal
    details_btn = page.locator('.o_form_view .o_data_row button:has-text("Details")')
    details_btn.first.click()
    page.wait_for_timeout(2000)
    _wait_no_loading(page)

    # In the detailed operations modal, fill serial numbers row by row
    modal = page.locator('.modal:visible').last
    rows = modal.locator('.o_data_row')

    for i in range(3):
        row = rows.nth(i)
        row.click()
        page.wait_for_timeout(300)
        lot_input = row.locator("[name='lot_name'] input").first
        lot_input.fill(SERIALS[i])
        lot_input.press("Tab")
        page.wait_for_timeout(500)

    # Save the detailed operations modal
    modal.locator('button:has-text("Save")').first.click()
    page.wait_for_timeout(1500)
    _wait_no_loading(page)

    # Validate the receipt
    page.locator('button:visible:has-text("Validate")').first.click()
    page.wait_for_timeout(2000)
    _wait_no_loading(page)

    # Handle any confirmation modal
    confirm_modal = page.locator(".modal:visible")
    if confirm_modal.count() > 0:
        primary = confirm_modal.last.locator("button.btn-primary:visible")
        if primary.count() > 0:
            primary.first.click()
            page.wait_for_timeout(2000)
            _wait_no_loading(page)


run_oracle(oracle)
