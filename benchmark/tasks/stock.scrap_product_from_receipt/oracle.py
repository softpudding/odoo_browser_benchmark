"""Oracle for stock.scrap_product_from_receipt."""

from benchmark.oracle_helpers import (
    clear_search_filters,
    click_list_row,
    ensure_list_view,
    login,
    navigate,
    run_oracle,
    _wait_no_loading,
)


def oracle(page):
    login(page)

    navigate(page, "/odoo/inventory")
    _wait_no_loading(page)
    page.wait_for_timeout(2000)

    # Click the Receipts header link in the kanban overview
    receipts_link = page.locator('.o_kanban_record a:has-text("Receipts")')
    if receipts_link.count() > 0:
        receipts_link.first.click()
    else:
        page.locator('.o_kanban_record:has-text("Receipts")').first.click()
    page.wait_for_timeout(3000)
    _wait_no_loading(page)

    # Wait for the transfers list to load
    page.wait_for_selector(
        ".o_list_view .o_data_row, .o_kanban_record, .o_nocontent_help",
        timeout=15000,
    )

    clear_search_filters(page)
    page.wait_for_timeout(1000)
    _wait_no_loading(page)

    ensure_list_view(page)
    page.wait_for_timeout(1000)

    click_list_row(page, "BENCH-SCRAP-REC-01")
    page.wait_for_timeout(1000)
    _wait_no_loading(page)

    # Open action menu (gear icon) and click Scrap
    page.locator(".o_cp_action_menus .dropdown-toggle").first.click()
    page.wait_for_timeout(500)
    page.locator('.dropdown-menu:visible .dropdown-item:has-text("Scrap")').first.click()
    page.wait_for_timeout(2000)
    _wait_no_loading(page)

    # Wait for scrap modal
    page.wait_for_selector(".modal:visible", timeout=10000)
    page.wait_for_timeout(1000)
    modal = page.locator(".modal:visible").last

    # Set product if not pre-filled (the modal may not auto-set it)
    prod_input = modal.locator(".o_field_widget[name='product_id'] input").first
    if prod_input.input_value() == "":
        prod_input.click()
        prod_input.fill('Steel Bracket 12"')
        page.wait_for_timeout(1000)
        dropdown = page.locator(".dropdown-menu .dropdown-item:visible, .ui-autocomplete .ui-menu-item:visible")
        dropdown.first.click()
        page.wait_for_timeout(1000)
        _wait_no_loading(page)

    # Fill scrap quantity
    qty_input = modal.locator(".o_field_widget[name='scrap_qty'] input").first
    qty_input.click()
    page.wait_for_timeout(200)
    qty_input.fill("")
    qty_input.fill("2")
    qty_input.press("Tab")
    page.wait_for_timeout(500)

    # Click "Scrap Products" button to validate
    modal.locator('button[name="action_validate"]').first.click()
    page.wait_for_timeout(3000)
    _wait_no_loading(page)


run_oracle(oracle)
